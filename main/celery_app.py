# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('parsers')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.task_routes = {
    'backend.parsers.tasks.update_asics': {'queue': 'create_asics'},
    'backend.parsers.tasks.update_asic_xml': {'queue': 'create_asics'},
    'backend.common.tasks.update_all_asic_info': {'queue': 'update'},
    'backend.common.tasks.update_asic_info': {'queue': 'update'},
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
