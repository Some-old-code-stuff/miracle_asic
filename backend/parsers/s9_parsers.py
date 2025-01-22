# -*- coding: utf-8 -*-
import requests
from io import StringIO, BytesIO
from django.conf import settings
from lxml import etree
from requests.auth import HTTPDigestAuth

from backend.common.models import ChainInfo, MeasureType, FanInfo, ErrorRule, AsicType
from backend.parsers.base_parser import BaseParser


class S9Parser(BaseParser):
    def get_error_rules(self, error_rule=None):
        return super(S9Parser, self).get_error_rules(ErrorRule.objects.filter(asic_type=AsicType.S9))

    def __init__(self, ip_address, username, password):
        self.info_uri = '/cgi-bin/minerStatus.cgi'

        BaseParser.__init__(self, ip_address, username, password)

    def authenticate(self):
        requests.get(self.get_uri('/index'), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        BaseParser.authenticate(self)

    def check(self):
        page = requests.get(self.get_uri('cgi-bin/get_system_info.cgi'),
                            auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        if page.status_code != 200:
            return False
        return 'S9' in page.json()['minertype']

    def get_json(self):
        # Получаем страницу и просто парсим все данные в json по таблице и тд
        page = requests.get(self.get_uri(self.info_uri), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        parser = etree.HTMLParser()
        page = etree.parse(BytesIO(page.text.encode('utf-8')), parser).getroot()

        result = {}

        for index, elem in enumerate(page.cssselect('.cbi-section-table')):
            key = elem.get('id', 'default_{}'.format(index))
            result[key] = {
                'titles': [],
                'rows': []
            }
            result[key]['titles'] = list(map(lambda th: th.text, elem.cssselect('.cbi-section-table-titles th')))

            for row in elem.cssselect('.cbi-section-table-row'):
                row_json = {}

                for div in row.cssselect('.cbi-value-field div'):
                    if div.text is None:
                        continue
                    row_json[div.get('id').replace('cbi-table-1-', '')] = div.text

                if len(row_json) == 0:
                    for td in row.cssselect('td.cbi-value-field'):
                        row_json[td.get('id').replace('cbi-table-1-', '')] = td.text

                result[key]['rows'].append(row_json)

        page = requests.get(self.get_uri('cgi-bin/get_system_info.cgi'),
                            auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)

        result['info'] = page.json()
        print(result)
        return result

    def set_asic_name(self):
        self.asic.asic_name = self.asic_info.json_info.json_data['info']['minertype']
        self.asic.save()

    def set_host_name(self):
        self.asic.host_name = self.asic_info.json_info.json_data['info']['hostname']
        self.asic.save()
        pass

    def set_pool_address(self):
        self.asic.pool_address = self.asic_info.json_info.json_data['ant_pools']['rows'][0]['url']
        self.asic.save()
        pass

    def set_pool_username(self):
        self.asic.pool_username = self.asic_info.json_info.json_data['ant_pools']['rows'][0]['user']
        self.asic.save()
        pass

    def set_pool_status(self):
        self.asic.pool_status = self.asic_info.json_info.json_data['ant_pools']['rows'][0]['status']
        self.asic.save()
        pass

    def set_full_rate(self):
        for row in self.asic_info.json_info.json_data['ant_devs']['rows']:
            if 'temp' not in row and 'Total' in row['chain']:
                self.asic.full_rate = float(row['rate'].replace(',', ''))
                self.asic.full_rate = MeasureType.convert(self.asic.full_rate, MeasureType.GH_S, MeasureType.TH_S)
                self.asic.save()
                return
        pass

    def set_fan_info(self):
        for fan in self.asic_info.json_info.json_data['ant_fans']['rows']:
            for key, value in fan.items():
                v = int(value.replace(',', ''))
                if v > 0:
                    try:
                        fan_info = self.asic.fan_info_set.get(name=key.replace('ant_', ''))
                        fan_info.speed=v
                        fan_info.save()
                    except FanInfo.DoesNotExist:
                        fan_info = FanInfo(name=key.replace('ant_', ''), speed=v, asic=self.asic)
                        fan_info.save()

        pass

    def set_chain_info(self):
        chains = self.asic.chain_info_set
        chain_list = list(chains.order_by('id').all())  # вызываем enumerate для индексов

        for index, row in enumerate(self.asic_info.json_info.json_data['ant_devs']['rows']):
            if 'temp' not in row and 'Total' in row['chain']:
                continue

            try:
                chain_info = chain_list[index]
            except IndexError:
                chain_info = ChainInfo(asic=self.asic)

            if row['temp'] is not None:
                try:
                    chain_info.temperature = int(row['temp'])
                except ValueError:
                    try:
                        chain_info.temperature = int(row['temp2'])
                    except ValueError:
                        chain_info.temperature = 0
            else:
                try:
                    chain_info.temperature = int(row['temp2'])
                except ValueError:
                    chain_info.temperature = 0

            chain_info.frequency = float(row['frequency'])
            chain_info.rate = float(row['rate'].replace(',', ''))
            chain_info.measure = MeasureType.TH_S
            chain_info.rate = MeasureType.convert(chain_info.rate, MeasureType.GH_S, MeasureType.TH_S)

            chain_info.all_chips = int(row['asic'])
            chain_info.working_chips = int(row['status'].count('o'))
            chain_info.wrong_chips = chain_info.all_chips - chain_info.working_chips
            chain_info.save()
        pass

    def reboot(self):
        requests.get(self.get_uri('/cgi-bin/reboot.cgi'), auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        pass

    def change_password(self, password):
        data = {'current_pw':self.password, 'new_pw':password, 'new_pw_ctrl':password}
        result = requests.post(self.get_uri('/cgi-bin/passwd.cgi'), data=data, auth=HTTPDigestAuth(self.username, self.password), timeout=settings.REQUESTS_TIMEOUT)
        super(S9Parser, self).change_password(password)
        print(result)
        pass
