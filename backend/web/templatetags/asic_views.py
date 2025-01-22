# -*- coding: utf-8 -*-


from django import template

register = template.Library()


@register.inclusion_tag('views/asic_dashboard_view.html')
def asic_dashboard_view(asic):
    return {
        'asic':asic
    }


@register.inclusion_tag('views/asic_table_view.html')
def asic_table_view(asic):
    return {
        'asic':asic
    }


@register.inclusion_tag('views/asic_modal_view.html')
def asic_modal_view(asic):
    return {'asic':asic}