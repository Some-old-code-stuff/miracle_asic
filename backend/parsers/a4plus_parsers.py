# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.db.models.aggregates import Sum

from backend.common.models import ChainInfo, ErrorRule, AsicType
from backend.parsers.base_parser import BaseParser


class A4PlusParser(BaseParser):
    def get_error_rules(self, error_rules=None):
        return super(A4PlusParser, self).get_error_rules(ErrorRule.objects.filter(asic_type=AsicType.A4PLUS))

    def __init__(self, ip_address, username, password):
        self.info_uri = '/cgi-bin/api.py'
        BaseParser.__init__(self, ip_address, username, password)

    def check(self):
        page = requests.get(self.get_uri(self.info_uri), timeout=10)
        try:
            page.json()
            return True
        except ValueError:
            return False

    def get_json(self):
        socket_json = self.socket_api.command('devs+pools')
        result = {
            'DEVS': socket_json['devs'][0]['DEVS'],
            'POOLS': socket_json['pools'][0]['POOLS'],
            'miner_conf': requests.get(self.get_uri('conf/miner.conf'), timeout=10).json()
        }

        return result

    def set_asic_name(self):
        self.asic.asic_name = 'A4+'
        self.asic.save()

    def set_host_name(self):
        self.asic.host_name = self.asic_info.json_info.json_data['POOLS'][0]['User']
        self.asic.save()
        pass

    def set_pool_address(self):
        self.asic.pool_address = self.asic_info.json_info.json_data['POOLS'][0]['URL']
        self.asic.save()
        pass

    def set_pool_username(self):
        self.asic.pool_username = self.asic_info.json_info.json_data['POOLS'][0]['User']
        self.asic.save()
        pass

    def set_pool_status(self):
        self.asic.pool_status = self.asic_info.json_info.json_data['POOLS'][0]['Status']
        self.asic.save()
        pass

    def set_full_rate(self):
        self.asic.full_rate = self.asic.chain_info_set.aggregate(sum=Sum('rate'))['sum']
        self.asic.save()

    def set_fan_info(self):
        if self.asic.fan_info_set.count() > 0:
            self.asic.fan_info_set.update(speed=55*int(self.asic_info.json_info.json_data['DEVS'][0]['DUTY']))
        else:
            self.asic.fan_info_set.create(name='Fan1', speed=55*int(self.asic_info.json_info.json_data['DEVS'][0]['DUTY']))

    def set_chain_info(self):
        chains = self.asic.chain_info_set
        chain_list = list(chains.order_by('id').all())  # вызываем enumerate для индексов

        for index, chain_json in enumerate(self.asic_info.json_info.json_data['DEVS']):
            try:
                chain_info = chain_list[index]
            except IndexError:
                chain_info = ChainInfo(asic=self.asic)
            chain_info.all_chips = chain_json['CHIP']
            chain_info.rate = float(chain_json['MHS av'])
            chain_info.temperature = int(chain_json['TempAVG'])
            chain_info.frequency = int(self.asic_info.json_info.json_data['miner_conf']['Frequency'])

            if chain_json['Enabled'] == 'Y':
                chain_info.working_chips = chain_info.all_chips
            else:
                chain_info.wrong_chips = chain_info.all_chips
            chain_info.save()

        pass

    def reboot(self):
        try:
            requests.post(self.get_uri('/cgi-bin/reboot.py'), timeout=settings.REQUESTS_TIMEOUT)
        except:
            pass