# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your tests here.

def get_info_page_s9():
    from backend.common.models import Asic, AsicType, CryptType

    a = Asic(type=AsicType.S9, crypt_type=CryptType.BITCOIN, ip_address='192.168.1.21')
    a.parser.authenticate()
    return a.parser.get_info()


def get_all_data():
    import requests
    from requests.auth import HTTPDigestAuth
    from StringIO import StringIO
    from lxml import etree

    s = requests.Session()

    s.get('http://192.168.1.21', auth=HTTPDigestAuth('root', 'root'))
    page = s.get('http://192.168.1.21/cgi-bin/minerStatus.cgi', auth=HTTPDigestAuth('root', 'root'))
    print(page.text)

    parser = etree.HTMLParser()
    page = etree.parse(StringIO(page.text.encode('utf-8')), parser).getroot()

    # page = BeautifulSoup(page.text, 'lxml')
    # print(page.text)

    for index, elem in enumerate(page.cssselect('.cbi-section-table')):
        print(index, elem.get('id', 'default'))

    # for elem in page.cssselect('table'):
    #     print(elem)
