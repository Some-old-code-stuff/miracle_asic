# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from crontab import CronTab
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from backend.common import tasks
from backend.common.models import Asic, AsicInfo, FanInfo, ChainInfo, Farm, Subnet, Client, AsicTypeRate, Error, ErrorRule, \
    UserProfile


def update_asic_info(modeladmin, request, queryset):
    for asic in queryset.values('pk').all():
        tasks.update_asic_info(asic['pk'])

update_asic_info.short_description = u"Обновить данные ASIC вручную"


@admin.register(Asic)
class AsicAdmin(admin.ModelAdmin):
    search_fields = ['name', 'ip_address', 'type', 'crypt_type']
    list_display = ['name', 'ip_address', 'type', 'crypt_type', 'last_info']
    list_filter = ('type', 'crypt_type')
    actions = [update_asic_info]

    def last_info(self, instance):
        """Function to display pretty version of our data"""

        info = instance.asic_info_history.last()

        if info is None:
            return ''

        # Convert the data to sorted, indented JSON
        response = json.dumps(info.json_info.json_data, sort_keys=True, indent=2)

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)


@admin.register(AsicInfo)
class AsicInfoAdmin(admin.ModelAdmin):
    search_fields = ['created', 'asic__name', 'asic__ip_address']
    list_display = ['created', 'get_asic_name', 'get_asic_ip_address', 'data_prettified', 'changed']
    list_filter = ('asic__ip_address', )
    readonly_fields = ('created', 'changed', 'data_prettified')
    list_per_page = 20

    def data_prettified(self, instance):
        """Function to display pretty version of our data"""

        # Convert the data to sorted, indented JSON
        response = json.dumps(instance.json_info.json_data, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        # response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style='colorful')

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)

    data_prettified.short_description = 'data prettified'

    def get_asic_ip_address(self, obj):
        return obj.asic.ip_address

    get_asic_ip_address.short_description = u'IP адрес ASIC'
    get_asic_ip_address.admin_order_field = 'asic__ip_address'

    def get_asic_name(self, obj):
        return obj.asic.name

    get_asic_name.short_description = u'Наименование ASIC'
    get_asic_name.admin_order_field = 'asic__name'


@admin.register(ChainInfo)
class ChainInfoAdmin(admin.ModelAdmin):
    search_fields = ['frequency', 'rate', 'temperature', 'measure', 'all_chips', 'asic__asic_name']
    list_display = ['frequency', 'rate', 'temperature', 'measure', 'all_chips', 'wrong_chips', 'working_chips']


@admin.register(FanInfo)
class FanInfoAdmin(admin.ModelAdmin):
    search_fields = ['name', 'speed', 'asic__asic_name']
    list_display = ['name', 'speed']


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name']


@admin.register(Subnet)
class SubnetAdmin(admin.ModelAdmin):
    search_fields = ['name', 'masks']
    list_display = ['name', 'masks']
    actions = ['write_cron_tab']

    def write_cron_tab(self, request, queryset):
        cron = CronTab(user=settings.CRON_USER)
        cron.remove_all()
        for farm in queryset.all():
            for mask in farm.masks.split(','):
                exclude = ''
                if farm.exclude_ips:
                    exclude = '--exclude {}'.format(farm.exclude_ips)

                command = '{} {}/farm_{}_asics_{}.xml {}.0-255 {}'.format(
                    settings.NMAP_COMMAND,
                    settings.NMAP_FILE_DIRECTORY,
                    farm.id,
                    mask.replace('.', '_'),
                    mask,
                    exclude
                )

                job = cron.new(command)
                job.minute.every(5)
        cron.write()


@admin.register(AsicTypeRate)
class AsicTypeRateAdmin(admin.ModelAdmin):
    search_fields = ['default_rate']
    list_display = ['type', 'default_rate', 'measure']
    list_filter = ('type', 'measure', )
    actions = ['set_default_rates']

    def set_default_rates(self, request, queryset):
        for default_rate in queryset.all():
            Asic.objects.filter(type=default_rate.type).update(default_rate=default_rate.default_rate, measure=default_rate.measure)


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    search_fields = ['message']
    list_display = ['asic', 'message']
    readonly_fields = ('asic', )


@admin.register(ErrorRule)
class ErrorRule(admin.ModelAdmin):
    list_filter = ('asic_type', )
    list_display = ['asic_type', 'field_name', 'value_type', 'comparison_type', 'value', 'percent', 'message']


admin.site.register(UserProfile)