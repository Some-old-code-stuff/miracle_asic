# -*- coding: utf-8 -*-
import requests
from django.conf import settings
from django.db.models.aggregates import Sum

from backend.common.models import ChainInfo, MeasureType, ErrorRule, AsicType
from backend.parsers.base_parser import BaseParser


class L21Parser(BaseParser):
    def get_error_rules(self, error_rule=None):
        return super(L21Parser, self).get_error_rules(ErrorRule.objects.filter(asic_type=AsicType.L21))

    def __init__(self, ip_address, username, password):
        self.info_uri = 'devs'
        BaseParser.__init__(self, ip_address, username, password)

    def check(self):
        page = requests.get(self.get_uri(self.info_uri), timeout=settings.REQUESTS_TIMEOUT)
        return page.status_code == 200

    def get_json(self):
        try:
            devs = self.socket_api.devs()['DEVS']
        except:
            raise requests.ConnectionError()

        miner = self.socket_api.pools()
        pools = miner['POOLS']
        status = miner['STATUS']
        # frequency = requests.get(self.get_uri('getfrequency'), timeout=settings.REQUESTS_TIMEOUT).json()
        chip_stats = self.socket_api.chipstat()['DEVS']
        all_chips = 36
        chip_stats = [
            {
                'workingChips': len([y for y in x.keys() if 'accept' in y])
            }
            for x in chip_stats
        ]

        # working_chips = len([x for x in chip_stats.keys() if 'accept' in x])
        # wrong_chips = all_chips - working_chips
        return {
            'devs': devs,
            'pools': pools,
            'status': status,
            'frequency': {
                'currentFrequency': 648,
                'chipNumber': all_chips,
                'chains':chip_stats
            }
        }

    def set_asic_name(self):
        self.asic.asic_name = 'L21'
        self.asic.save()

    def set_host_name(self):
        self.asic.host_name = self.asic_info.json_info.json_data['pools'][0]['User']
        self.asic.save()
        pass

    def set_pool_address(self):
        self.asic.pool_address = self.asic_info.json_info.json_data['pools'][0]['URL']
        self.asic.save()
        pass

    def set_pool_username(self):
        self.asic.pool_username = self.asic_info.json_info.json_data['pools'][0]['User']
        self.asic.save()
        pass

    def set_pool_status(self):
        self.asic.pool_status = self.asic_info.json_info.json_data['pools'][0]['Status']
        self.asic.save()
        pass

    def set_full_rate(self):
        self.asic.full_rate = self.asic.chain_info_set.aggregate(sum=Sum('rate'))['sum'] or 0
        self.asic.save()

    def set_chain_info(self):
        chains = self.asic.chain_info_set
        chain_list = list(chains.order_by('id').all())  # вызываем enumerate для индексов

        for index, chain_json in enumerate(self.asic_info.json_info.json_data['devs']):
            rate = float(chain_json['MHS 1m'])

            if settings.ENABLE_CONVERTATION_FOR_L21:
                rate = rate * 2 ** 20 / 10 ** 6

            try:
                chain_info = chain_list[index]
            except IndexError:
                chain_info = ChainInfo(asic=self.asic)

            chain_info.rate = rate
            chain_info.temperature = chain_json['temperature']
            chain_info.frequency = int(self.asic_info.json_info.json_data['frequency']['currentFrequency'])
            chain_info.all_chips = int(self.asic_info.json_info.json_data['frequency']['chipNumber'])
            chain_info.working_chips = int(self.asic_info.json_info.json_data['frequency']['chains'][index]['workingChips'])
            chain_info.wrong_chips = chain_info.all_chips - chain_info.working_chips
            chain_info.save()
        pass

    def reboot(self):
        requests.get(self.get_uri('restart'), timeout=settings.REQUESTS_TIMEOUT)

    def change_password(self, password):
        data = {'UserNameOld': self.username, 'PasswordOld': self.password, 'UserNameNew': self.username,
                'PasswordNew': password}
        print(data)
        result = requests.post(self.get_uri('saveSys'), data=data, timeout=settings.REQUESTS_TIMEOUT)
        print(result, result.json())
        super(L21Parser, self).change_password(password)
