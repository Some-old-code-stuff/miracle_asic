# -*- coding: utf-8 -*-


# start nmap
# nmap -F -T5 -oX ports.xml 192.168.1.0-255
# wait for output
# read output get ips
# host > address [addr]
import re

from lxml import etree
from requests import ReadTimeout

from backend.parsers.a4plus_parsers import A4PlusParser
from backend.parsers.dr100_parsers import DR100Parser
from backend.parsers.l21_parsers import L21Parser
from backend.parsers.l3plus_parsers import L3PlusParser
from backend.parsers.s9_parsers import S9Parser
from requests import ConnectionError

from backend.common.models import AsicType, Asic, AsicTypeRate, AlgorithmType
from backend.parsers.d3_parsers import BaseD3Parser
from main.local_settings import NMAP_FILE_NAME


class AsicUpdater:
    @staticmethod
    def parsers():
        return {
            AsicType.DR100: DR100Parser,
            AsicType.A4PLUS: A4PlusParser,
            AsicType.L21: L21Parser,
            AsicType.D3: BaseD3Parser,
            AsicType.S9: S9Parser,
            AsicType.L3PLUS: L3PlusParser,
        }

    @staticmethod
    def alghorithms():
        return{
            AsicType.DR100: AlgorithmType.X11,
            AsicType.A4PLUS: AlgorithmType.SCRYPT,
            AsicType.L21: AlgorithmType.SCRYPT,
            AsicType.D3: AlgorithmType.X11,
            AsicType.S9: AlgorithmType.SHA_256,
            AsicType.L3PLUS: AlgorithmType.SCRYPT,
        }

    def update_asics(self, file_name=NMAP_FILE_NAME):
        match = re.search('farm_(?P<farm_id>\d+)_', file_name)
        if match is None:
            return
        farm_id = match.group('farm_id')
        tree = etree.parse(file_name)
        for el in tree.findall('.//host//address[@addr]'):
            ip_address = el.attrib['addr']
            print(ip_address)
            for asic_type, parser_class in AsicUpdater.parsers().items():
                if asic_type is AsicType.S9:
                    username = 'root'
                    password = 'root'
                    if ip_address == '192.168.1.21':
                        password = ''
                elif asic_type is AsicType.A4PLUS:
                    username = 'root'
                    password = 'root'
                elif asic_type is AsicType.D3:
                    username = 'root'
                    password = 'root'
                elif asic_type is AsicType.DR100:
                    username = 'admin'
                    password = 'admin'
                elif asic_type is AsicType.L3PLUS:
                    username = 'root'
                    password = 'root'
                elif asic_type is AsicType.L21:
                    username = 'root'
                    password = 'root'

                try:
                    if parser_class(ip_address, username, password).check():
                        Asic.objects.get(ip_address=ip_address)
                except ConnectionError as e:
                    print(e)
                    break
                except ValueError as e:
                    print(e)
                except ReadTimeout as e:
                    print(e)
                except Asic.DoesNotExist:
                    asic = Asic(ip_address=ip_address, name=ip_address, type=asic_type, alg_type=AsicUpdater.alghorithms()[asic_type])

                    asic.username = username
                    asic.password = password
                    asic.save()
                    asic_type_rate = AsicTypeRate.objects.filter(type=asic_type).first()

                    if asic_type_rate is not None:
                        asic.default_rate = asic_type_rate.default_rate
                        asic.measure = asic_type_rate.measure

                    asic.save()
                    break
