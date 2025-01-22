# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from backend.parsers.d3_parsers import BaseD3Parser


def test_dr3():
    dr3_parser = BaseD3Parser('192.168.9.17')
    return dr3_parser.get_info()


def test_mask_finding():
    # start nmap
    # nmap -F -T5 -oX ports.xml 192.168.1.0-255
    # wait for output
    # read output get ips
    # host > address [addr]



    import requests
    for i in range(0,255):
        a = requests.get('http://192.168.1.{}'.format(i))
        print(a.content.decode())