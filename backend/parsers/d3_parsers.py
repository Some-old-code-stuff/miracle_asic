# -*- coding: utf-8 -*-

import requests
from django.conf import settings
from requests.auth import HTTPDigestAuth

from backend.common.models import ChainInfo, MeasureType, FanInfo, ErrorRule, AsicType
from backend.parsers.base_parser import BaseParser


class BaseD3Parser(BaseParser):
    def get_error_rules(self, error_rule=None):
        return super(BaseD3Parser, self).get_error_rules(ErrorRule.objects.filter(asic_type=AsicType.D3))

    def __init__(self, ip_address,username, password):
        BaseParser.__init__(self, ip_address, username, password)
        self.info_uri = 'cgi-bin/get_status_api.cgi'

    def check(self):
        page = requests.get(self.get_uri('cgi-bin/get_system_info.cgi'), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        if page.status_code != 200:
            return False
        return 'D3' in page.json()['minertype']

    def get_json(self):
        # Получаем страницу и просто парсим все данные в json по таблице и тд
        page = requests.get(self.get_uri(self.info_uri), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT).content.decode()

        result = []

        for table in page.replace('\n', '').split('|'):
            table_data = {}
            for index, data in enumerate(table.split(',')):
                try:
                    key, value = data.split('=')
                except ValueError:
                    key = 'undefined_field_{}'.format(index)
                    value = data
                table_data[key]=value

            result.append(table_data)

        page = requests.get(self.get_uri('cgi-bin/get_system_info.cgi'),
                            auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)

        print(page.content)

        result.append(page.json())
        return result

    def get_asic_name(self, json):
        for row in json:
            if 'minertype' in row:
                return row['minertype']
        return ''

    def get_host_name(self, json):
        for row in json:
            if 'hostname' in row:
                return row['hostname']
        return ''

    def get_pool_status(self, json):
        for row in json:
            if 'Stratum URL' in row:
                return row['Status']
        return ''

    def get_pool_address(self, json):
        for row in json:
            if 'Stratum URL' in row:
                return row['URL']
        return ''

    def get_pool_username(self, json):
        for row in json:
            if 'Stratum URL' in row:
                return row['User']
        return ''

    def get_full_rate(self, json):
        for row in json:
            if 'GHS av' in row:
                return MeasureType.convert(float(row['GHS av']), MeasureType.MH_S, MeasureType.GH_S)
        return 0

    def set_asic_name(self):
        self.asic.asic_name = self.get_host_name(self.asic_info.json_info.json_data)
        self.asic.save()

    def set_host_name(self):
        self.asic.host_name = self.get_host_name(self.asic_info.json_info.json_data)
        self.asic.save()
        pass

    def set_pool_address(self):
        self.asic.pool_address = self.get_pool_address(self.asic_info.json_info.json_data)
        self.asic.save()
        pass

    def set_pool_username(self):
        self.asic.pool_username = self.get_pool_username(self.asic_info.json_info.json_data)
        self.asic.save()
        pass

    def set_pool_status(self):
        self.asic.pool_status = self.get_pool_status(self.asic_info.json_info.json_data)
        self.asic.save()
        pass

    def set_full_rate(self):
        self.asic.full_rate = self.get_full_rate(self.asic_info.json_info.json_data)
        self.asic.save()

    def set_fan_info(self):
        for row in self.asic_info.json_info.json_data:
            if 'STATS' in row:
                for i in range(1,int(row['fan_num'])+1):
                    key='fan{}'.format(i)
                    try:
                        fan_info = self.asic.fan_info_set.get(name=key)
                    except FanInfo.DoesNotExist:
                        fan_info = FanInfo(name=key, asic=self.asic)
                    fan_info.speed = row[key]
                    fan_info.save()

    def set_chain_info(self):
        chains = self.asic.chain_info_set
        chain_list = list(chains.order_by('id').all())  # вызываем enumerate для индексов

        for row in self.asic_info.json_info.json_data:
            if 'STATS' in row:
                for i in range(1,4):
                    try:
                        chain_info = chain_list[i]
                    except IndexError:
                        chain_info = ChainInfo(asic=self.asic)
                    chain_info.temperature = int(row['temp{}'.format(i)])
                    chain_info.frequency = int(row['frequency'])
                    chain_info.rate = float(row['chain_rate{}'.format(i)].replace(',', ''))
                    chain_info.measure = MeasureType.GH_S
                    chain_info.rate = MeasureType.convert(chain_info.rate, MeasureType.MH_S, MeasureType.GH_S)

                    chain_info.all_chips = int(row['chain_acn{}'.format(i)])
                    chain_info.working_chips = int(row['chain_acs{}'.format(i)].count('o'))
                    chain_info.wrong_chips = chain_info.all_chips - chain_info.working_chips
                    chain_info.save()

    def reboot(self):
        requests.get(self.get_uri('/cgi-bin/reboot.cgi'), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        pass

    def change_password(self, password):
        data = {'current_pw':self.password, 'new_pw':password, 'new_pw_ctrl':password}
        result = requests.post(self.get_uri('/cgi-bin/passwd.cgi'), auth=HTTPDigestAuth(self.username, self.password), data=data, timeout=settings.REQUESTS_TIMEOUT)
        super(BaseD3Parser, self).change_password(password)
        print(result)

