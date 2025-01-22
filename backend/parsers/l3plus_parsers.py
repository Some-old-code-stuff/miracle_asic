# -*- coding: utf-8 -*-
import re

import requests
from django.conf import settings
from requests.auth import HTTPDigestAuth

from backend.common.models import MeasureType, ChainInfo, FanInfo, ErrorRule, AsicType
from backend.parsers.s9_parsers import S9Parser


# Потому что в l3+ и s9 используется antminer
# TODO возможно, стоит объединить по типу прошивок, а не типу асиков
class L3PlusParser(S9Parser):
    def get_error_rules(self, error_rule=None):
        return super(S9Parser, self).get_error_rules(ErrorRule.objects.filter(asic_type=AsicType.L3PLUS))

    def __init__(self, ip_address, username, password):
        S9Parser.__init__(self, ip_address, username, password)

    def check(self):
        page = requests.get(self.get_uri('cgi-bin/get_system_info.cgi'), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        if page.status_code != 200:
            return False
        return 'L3+' in page.json()['minertype']

    def set_full_rate(self):
        self.asic.full_rate = float(self.asic_info.json_info.json_data['default_0']['rows'][0]['ant_ghsav'])
        self.asic.save()
        pass

    def set_fan_info(self):
        for fan in self.asic_info.json_info.json_data['ant_fans']['rows']:
            for key, value in fan.items():
                if value is None:
                    continue
                v = int(value.replace(',', ''))
                if v > 0:
                    try:
                        fan_info = self.asic.fan_info_set.get(name=key.replace('ant_', ''))
                        fan_info.speed=v
                        fan_info.save()
                    except FanInfo.DoesNotExist:
                        fan_info = FanInfo(name=key.replace('ant_', ''), speed=v, asic=self.asic)
                        fan_info.save()

    def set_chain_info(self):
        chains = self.asic.chain_info_set
        chain_list = list(chains.order_by('id').all())  # вызываем enumerate для индексов
        for index, row in enumerate(self.asic_info.json_info.json_data['ant_devs']['rows']):
            try:
                chain_info = chain_list[index]
            except IndexError:
                chain_info = ChainInfo(asic=self.asic)

            chain_info.temperature = int(re.search('O:(?P<temp>\d+)', row['temp2']).group('temp'))

            chain_info.frequency = float(row['frequency'])
            chain_info.rate = float(row['rate'].replace(',', ''))
            chain_info.measure = MeasureType.MH_S

            chain_info.all_chips = int(row['asic'])
            chain_info.working_chips = int(row['status'].count('o'))
            chain_info.wrong_chips = chain_info.all_chips - chain_info.working_chips
            chain_info.save()