# -*- coding: utf-8 -*-
import glob

from celery import shared_task

from backend.common.models import Asic
from backend.parsers.update_asics import AsicUpdater
from main.local_settings import NMAP_MASK


@shared_task
def update_asics():
    for xml in glob.glob(NMAP_MASK):
        update_asic_xml.delay(xml)


@shared_task
def update_asic_xml(xml):
    print(xml)
    AsicUpdater().update_asics(xml)


def update_asics_info():
    for asic in Asic.objects.filter(stop_update=False).all():
        asic.update_info()
