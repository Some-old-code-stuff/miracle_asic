# -*- coding: utf-8 -*-
import hashlib
import random
from datetime import timedelta

import requests
from django.conf import settings
from django.db.models import Count
from django.utils import timezone

import backend.common.models as models


def send_sms(message, raw_phone):
    address = 'https://sms.ru/sms/send'
    import re
    string = ''
    phone = string.join(re.findall('\d', raw_phone))

    data = {
        'api_id': settings.API_ID,
        'to': phone,
        'msg': message,
        'json': 1}
    print(data)
    result = requests.get(address, params=data)
    print(result.json())

    return result


def send_token(phone):
    token = str(random.randrange(1, 9999)).zfill(4)
    print(token)
    profile = models.UserProfile.objects.get(phone=phone)
    profile.sms_token = hashlib.sha256(token.encode()).hexdigest()
    profile.sms_token_expiration = timezone.now() + timedelta(minutes=10)
    profile.sms_token_try_count = 3
    profile.save()
    if not settings.DEBUG:
        send_sms(token, phone)
    return token


def check_token(phone, token):
    try:
        profile = models.UserProfile.objects.get(phone=phone)
    except models.UserProfile.DoesNotExist:
        return False, 0

    if profile.sms_token_try_count == 0 or profile.sms_token_try_count is None:
        return False, 0

    token_sha = hashlib.sha256(token.encode()).hexdigest()
    now = timezone.now()
    print(profile.sms_token, token_sha)
    if profile.sms_token == token_sha and now < profile.sms_token_expiration:
        profile.sms_token = None
        profile.sms_token_verification = None
        profile.sms_token_try_count = None
        profile.save()
        return True, None
    profile.sms_token_try_count -= 1
    profile.save()
    return False, profile.sms_token_try_count


def update_passwords():
    for asic in models.Asic.objects.all():
        if asic.ip_address == '192.168.1.21':
            continue
        if asic.type is models.AsicType.S9:
            asic.username = 'root'
            asic.password = 'root'
        elif asic.type is models.AsicType.A4PLUS:
            asic.username = 'root'
            asic.password = 'root'
        elif asic.type is models.AsicType.D3:
            asic.username = 'root'
            asic.password = 'root'
        elif asic.type is models.AsicType.DR100:
            asic.username = 'admin'
            asic.password = 'admin'
        elif asic.type is models.AsicType.L3PLUS:
            asic.username = 'root'
            asic.password = 'root'
        elif asic.type is models.AsicType.L21:
            asic.username = 'root'
            asic.password = 'root'
        asic.save()


def send_socket(ip_address='192.168.1.41', command='summary', port=4028):
    import socket
    import json
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip_address, 4028))
    sock.send(json.dumps({'command': command}).encode())
    # sock.send(''.encode())
    resp = ''
    while 1:
        buf = sock.recv(4096)
        print(buf.decode())
        if buf:
            resp += buf.decode()
        else:
            break
    print(resp)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print(json.loads(resp[:-1]))


def convert_to_csv(file='/home/mrakolice/Projects/miracle_asic/asics.csv'):
    import csv
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for farm in models.Farm.objects.all():
            writer.writerow([farm.name, farm.asic_set.count()])
            asics = farm.asic_set.values('client__name', 'type').annotate(count=Count('type'))
            print(asics)
            for asic in asics:
                writer.writerow([asic['client__name'], models.AsicType.get_item(asic['type']), asic['count']])

