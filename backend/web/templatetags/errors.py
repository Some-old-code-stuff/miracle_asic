# -*- coding: utf-8 -*-


from django import template

from backend.common.models import FieldName

register = template.Library()


@register.simple_tag
def have_errors(asic, field_name=None, object_id=None):
    if field_name is None:
        if asic.open_errors.count() > 0:
            return 'error'
        if asic.open_warnings.count() > 0:
            return 'warning'
        return ''

    print(field_name, object_id)

    if asic.open_errors.filter(error_rule__field_name=field_name, object_id=object_id).count() > 0:
        return 'danger'

    if asic.open_warnings.filter(error_rule__field_name=field_name, object_id=object_id).count() > 0:
        return 'warning'

    return 'success'


@register.simple_tag
def have_errors_with_warnings(asic, field_name, object_id=None):
    warnings = asic.open_warnings.filter(error_rule__field_name=field_name, object_id=object_id)
    warning_count = warnings.count()
    if warning_count == 0:
        return 'success'
    error_rule = warnings.first().error_rule

    error_count = asic.open_errors.filter(error_rule__field_name=FieldName.ERROR_RULE_COUNT, error_rule__error_rule=error_rule).count()
    if error_count > 0:
        return 'danger'

    return 'warning'


@register.filter
def have_connect_error(asic):
    if asic.has_connect_error():
        return 'red-icon'
    if asic.has_connect_warning():
        return 'yellow-icon'

    return ''


@register.filter
def have_connect_error_title(asic):
    if asic.has_connect_error():
        return 'ASIC недоступен!'
    if asic.has_connect_warning():
        return 'ASIC был недоступен какое-то время назад!'

    return 'ASIC доступен'
