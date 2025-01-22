# -*- coding: utf-8 -*-


from django import template

register = template.Library()


@register.inclusion_tag('views/error_table_view.html')
def error_table_view(error):
    return {
        'error': error
    }


@register.inclusion_tag('views/error_dashboard_view.html')
def error_dashboard_view(error):
    return {
        'error': error
    }


@register.inclusion_tag('views/error_history_view.html')
def error_history_view(modal_name, modal_id, errors, tabindex=None):
    if tabindex is None:
        tabindex = -2

    return {
        'modal_name': modal_name,
        'modal_id': modal_id,
        'errors': errors,
        'tabindex': tabindex,
    }
