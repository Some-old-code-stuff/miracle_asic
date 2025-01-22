# -*- coding: utf-8 -*-
import socket
from itertools import chain

from django.db.models import Q, Count
from django.utils import timezone
from requests import ConnectionError
from requests import ReadTimeout

from backend.common.models import AsicInfo, ErrorRule, AsicType, AsicTypeRate, FieldName, JsonInfo
from backend.parsers.socket_api import SocketApi


class ValidationRule(object):
    def __init__(self, func, message, error_rule=None):
        self.message = message
        self.func = func
        self.error_rule = error_rule

    def validate(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class BaseParser(object):
    def get_error_rules(self, error_rules=None):
        # Убираем дубликаты правил
        # Нам нужны правила с одинаковыми проверяемыми значениями
        # А еще и с разным типом сравнения... Потому что есть разные правила на разные вещи.
        # По факту, нужно найти данные, совпадающие везде, кроме значения\процента\сообщения об ошибке
        # Если это "Количество ошибок по правилу", тогда с совпадающим проверяемым правилом
        default_rules = ErrorRule.objects.filter(asic_type=AsicType.UNDEFINED)
        if error_rules is None:
            return default_rules
        result_rules = error_rules | default_rules
        # Находим дубликаты значений
        simple_rules = result_rules.filter(~Q(field_name=FieldName.ERROR_RULE_COUNT))\
            .order_by('field_name', 'error_level', 'value_type', 'comparison_type', '-asic_type') \
            .distinct('field_name', 'error_level', 'value_type', 'comparison_type')
        complicated_rules = result_rules.filter(field_name=FieldName.ERROR_RULE_COUNT)\
            .order_by('error_level', 'error_rule', 'value_type', 'comparison_type', '-asic_type') \
            .distinct('error_level', 'error_rule', 'value_type', 'comparison_type')

        return list(chain(simple_rules, complicated_rules))

    def __init__(self, ip_address, username, password):
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.__is_authenticate = False
        self.validation_rules = []
        self.asic_info = None
        self.error_rules = self.get_error_rules()
        self.init_validation()
        self.connection_error = None
        self.socket_api = SocketApi(ip_address)
        pass

    def init_validation(self):
        for error_rule in self.error_rules:
            self.add_validation_error_rule(error_rule)

    def get_uri(self, uri):
        return 'http://{}/{}'.format(self.ip_address, uri)

    def check(self):
        return False

    def check_auth(func):
        def func_wrapper(self):
            if self.__is_authenticate:
                return func
            self.authenticate()

        return func_wrapper

    def authenticate(self):
        self.__is_authenticate = True
        pass

    def get_json(self):
        # авторизация
        # получаем страницу
        # парсим данные со страницы
        return {'base_parser': 'undefined_data'}

    def set_asic_name(self):
        pass

    def set_host_name(self):
        pass

    def set_pool_address(self):
        pass

    def set_pool_username(self):
        pass

    def set_pool_status(self):
        pass

    def set_full_rate(self):
        pass

    def set_fan_info(self):
        pass

    def set_chain_info(self):
        pass

    def get_info(self):
        self.connection_error = None
        try:
            json_data = self.get_json()
        except (ConnectionError, ReadTimeout, socket.timeout):
            json_data = {'undefined_data': 'undefined_data'}
            self.connection_error = u'Невозможно получить информацию от ASIC. Проблемы с соединением.'

        self.asic_info = AsicInfo(
            created=timezone.now(),
            changed=timezone.now(),
            asic=self.asic,
        )
        self.asic_info.save()
        self.asic_info.json_info = JsonInfo(json_data=json_data)
        self.asic_info.json_info.save()
        if self.connection_error is not None:
            # 'connect'
            self.asic.add_error(message=self.connection_error, field_name=FieldName.CONNECT_ERROR)
            return

        self.set_asic_name()
        self.set_host_name()
        self.set_pool_address()
        self.set_pool_username()
        self.set_pool_status()

        self.set_fan_info()
        self.set_chain_info()

        self.set_full_rate()

        return self.asic_info

    def update(self, asic):
        self.asic = asic
        print(self.asic.ip_address)
        self.get_info()
        if self.connection_error is None:
            asic.down_level_connect_error()
        else:
            return self.asic_info

        self.asic.updated = timezone.now()

        if self.asic.default_rate == 0.0:
            asic_type_rate = AsicTypeRate.objects.filter(type=self.asic.type).first()

            if asic_type_rate is not None:
                self.asic.default_rate = asic_type_rate.default_rate
                self.asic.measure = asic_type_rate.measure
        self.asic.asic_info = self.asic_info
        self.asic.save()

        self.validate()
        return self.asic_info

    def add_validation_rule(self, func, message):
        self.validation_rules.append(ValidationRule(func, message))

        return self

    def add_validation_error_rule(self, error_rule):
        self.validation_rules.append(ValidationRule(error_rule.convert_to_func(), error_rule.message, error_rule))

    def validate(self):
        for rule in self.validation_rules:
            result = rule.validate(self.asic)
            for validate_result in result:
                have_error = validate_result[0]
                error_message = validate_result[1]
                try:
                    object_id = validate_result[2]
                except IndexError:
                    object_id = None

                if have_error:
                    print(object_id, have_error, error_message, self.asic_info)
                    self.asic.add_error(message=error_message, rule=rule.error_rule, object_id=object_id)
                else:
                    print('down level', validate_result, rule.error_rule.id)
                    self.asic.down_level_error(rule.error_rule, object_id)
                    pass

    def reboot(self):
        pass

    def change_password(self, password):
        self.password = password
        pass


class UndefinedParser(BaseParser):
    def __init__(self, ip_address):
        BaseParser.__init__(self, ip_address, '', '')

    def authenticate(self):
        # log usage and full stack
        pass

    def get_json(self):
        # log usage and full stack
        return {'undefined_parser': 'undefined_data'}
