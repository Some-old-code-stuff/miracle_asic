# -*- coding: utf-8 -*-
from celery import shared_task
from django.utils import timezone

from backend.common.models import Asic


@shared_task
def update_asic_info(asic_id):
    try:
        print(asic_id)
        Asic.objects.get(pk=asic_id).update_info()
    except Asic.DoesNotExist:
        return


@shared_task
def update_all_asic_info():
    Asic.objects.filter(resume_update_date__lte=timezone.now()).update(resume_update_date=None, stop_update=False)

    asics = Asic.objects.values('pk').filter(stop_update=False).all()
    for asic in asics:
        update_asic_info.delay(asic['pk'])

@shared_task
def reboot_asic(asic_id):
    try:
        Asic.objects.get(pk=asic_id).reboot()
    except Asic.DoesNotExist:
        return