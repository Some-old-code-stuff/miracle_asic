# -*- coding: utf-8 -*-
from django.conf import settings
from django.urls import reverse
from menu import Menu
from menu import MenuItem

from backend.common.models import Error


def generate_navigation():
    Menu.add_item('web', MenuItem(u'Все устройства', reverse('home'), weight=10, separator=True, icon='tools'))
    Menu.add_item('web', MenuItem(u'Устройства с ошибками', reverse('dashboard'), weight=10, separator=True, icon='tools'))
    error_count = Error.get_current_errors().count()
    warning_count = Error.get_current_warnings().count()
    Menu.add_item('web', MenuItem(u'Тип ошибки ({})'.format(error_count), reverse('errors'), weight=10, separator=True, icon='tools'))
    Menu.add_item('web', MenuItem(u'Нужно решить ({})'.format(warning_count), reverse('warnings'), weight=10, separator=True, icon='tools'))
    Menu.add_item('web', MenuItem(u'Мониторинг автоматического обновления', settings.FLOWER_URL, weight=10, separator=True, icon='tools'))
    Menu.add_item('web', MenuItem(u'Админка', reverse('admin:index'), weight=10, separator=True, icon='tools'))
    Menu.add_item('web', MenuItem(u'Выход', reverse('logout'), weight=10, separator=True, icon='tools'))


generate_navigation()