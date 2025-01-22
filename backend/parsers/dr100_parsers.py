# -*- coding: utf-8 -*-
import requests
from django.conf import settings

from backend.common.models import MeasureType, ErrorRule, AsicType
from backend.parsers.base_parser import BaseParser


class DR100Parser(BaseParser):
    def get_error_rules(self, error_rule=None):
        return super(DR100Parser, self).get_error_rules(ErrorRule.objects.filter(asic_type=AsicType.DR100))

    def __init__(self, ip_address, username, password):
        self.info_uri = 'cgi-bin/dashboard.cgi'
        BaseParser.__init__(self, ip_address, username, password)

    def check(self):
        page = requests.get(self.get_uri(self.info_uri), timeout=settings.REQUESTS_TIMEOUT)
        try:
            page.json()
            return True
        except ValueError:
            return False

    def get_json(self):
        dashboard_json = requests.get(self.get_uri(self.info_uri), timeout=settings.REQUESTS_TIMEOUT).json()
        network_conf = requests.get(self.get_uri('cgi-bin/local_setting.cgi'),
                                    timeout=settings.REQUESTS_TIMEOUT).json()  # hostname
        status_json = requests.get(self.get_uri('cgi-bin/status.cgi'), timeout=settings.REQUESTS_TIMEOUT).json()

        return {
            'dashboard': dashboard_json,
            'network_conf': network_conf,
            'status_json': status_json
        }

    def set_asic_name(self):
        self.asic.asic_name = 'DR100'
        self.asic.save()

    def set_host_name(self):
        self.asic.host_name = self.asic_info.json_info.json_data['network_conf']['hostname']
        self.asic.save()
        pass

    def set_pool_address(self):
        self.asic.pool_address = self.asic_info.json_info.json_data['dashboard']['miner_ip']
        self.asic.save()
        pass

    def set_pool_username(self):
        self.asic.pool_username = self.asic_info.json_info.json_data['dashboard']['miner_username']
        self.asic.save()
        pass

    def set_pool_status(self):
        self.asic.pool_status = 'Alive' if float(
            self.asic_info.json_info.json_data['dashboard']['network_delay']) < 5000 else 'None'
        self.asic.save()
        pass

    def set_full_rate(self):
        list = self.asic_info.json_info.json_data['dashboard']['hashrate_list'][5::]
        self.asic.full_rate = MeasureType.convert(sum(list) / float(len(list)), MeasureType.MH_S, MeasureType.GH_S)
        self.asic.save()
        pass

    def set_fan_info(self):
        if self.asic.fan_info_set.count() > 0:
            self.asic.fan_info_set.filter(name='Fan1').update(
                speed=int(self.asic_info.json_info.json_data['dashboard']['fanspeed']))
            self.asic.fan_info_set.filter(name='Fan2').update(
                speed=int(self.asic_info.json_info.json_data['dashboard']['fanspeed2']))
        else:
            self.asic.fan_info_set.create(name='Fan1', speed=int(self.asic_info.json_info.json_data['dashboard']['fanspeed']))
            self.asic.fan_info_set.create(name='Fan2', speed=int(self.asic_info.json_info.json_data['dashboard']['fanspeed2']))
        pass

    def set_chain_info(self):
        chains = self.asic.chain_info_set
        chain_list = list(chains.order_by('id').all())  # вызываем enumerate для индексов

        for i in range(1, 5):
            print(i)
            if 'temperature_unit{}'.format(i) in self.asic_info.json_info.json_data['dashboard']:
                all_chips = [x for x in self.asic_info.json_info.json_data['status_json'] if x['x'] == i - 1 and x['y'] < 18]
                working_chips = [x for x in all_chips if (x["accept"] + x["failed"]) > 0 and 0 <= x["failed"] * 100 / (
                x["accept"] + x["failed"]) <= 15]

                wrong_chips = len(all_chips) - len(working_chips)
                print(len(all_chips), len(working_chips), wrong_chips)

                try:
                    chain_list[i - 1].temperature = int(
                        self.asic_info.json_info.json_data['dashboard']['temperature_unit{}'.format(i)])
                    chain_list[i - 1].rate = self.asic.full_rate / 4
                    chain_list[i - 1].working_chips = len(working_chips)
                    chain_list[i - 1].wrong_chips = wrong_chips
                    chain_list[i - 1].frequency = int(self.asic_info.json_info.json_data['dashboard']['frq'] / 2)
                    chain_list[i - 1].save()
                except IndexError:
                    chains.create(
                        temperature=int(self.asic_info.json_info.json_data['dashboard']['temperature_unit{}'.format(i)]),
                        rate=self.asic.full_rate / 4,
                        working_chips=len(working_chips),
                        wrong_chips=wrong_chips,
                        all_chips=18,
                        frequency=int(self.asic_info.json_info.json_data['dashboard']['frq'] / 2),
                        measure=MeasureType.GH_S
                    )
            else:
                try:
                    chain_list[i - 1].temperature = 120
                    chain_list[i - 1].rate = 0
                    chain_list[i - 1].wrong_chips = 18
                    chain_list[i - 1].frequency = 0
                    chain_list[i - 1].save()
                except IndexError:
                    chains.create(
                        temperature=120,
                        rate=0,
                        wrong_chips=18,
                        all_chips=18,
                        frequency=0
                    )
        pass

    def reboot(self):
        requests.get(self.get_uri('/cgi-bin/save_miner_setting.cgi?action=1'), timeout=settings.REQUESTS_TIMEOUT)

    def change_password(self, password):
        requests.get(self.get_uri('/cgi-bin/change_password.cgi?password='+password), timeout=settings.REQUESTS_TIMEOUT)
        super(DR100Parser, self).change_password(password)