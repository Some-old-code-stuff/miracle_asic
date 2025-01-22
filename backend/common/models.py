# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import timedelta, datetime
from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import F
from django.db.models import OuterRef, Count
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.functional import cached_property


class UserProfile(models.Model):
    user = models.ForeignKey(auth_models.User, on_delete=models.CASCADE)
    sms_token = models.CharField(max_length=64, null=True, blank=True)
    sms_token_expiration = models.DateTimeField(null=True, blank=True)
    sms_token_try_count = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)


class AsicType:
    def __init__(self):
        pass

    UNDEFINED = 0
    S9 = 1
    L3PLUS = 2
    DR100 = 3
    A4PLUS = 4
    L21 = 5
    D3 = 6

    @staticmethod
    def get_items():
        return {
            AsicType.UNDEFINED: u'Не определен',
            AsicType.S9: u'S9',
            AsicType.L3PLUS: u'L3+',
            AsicType.DR100: u'DR100',
            AsicType.A4PLUS: u'A4+',
            AsicType.L21: u'L21',
            AsicType.D3: u'D3',
        }

    @staticmethod
    def get_item(item):
        return AsicType.get_items()[item]


class CryptType:
    def __init__(self):
        pass

    UNDEFINED = 0
    BITCOIN = 1
    LITECOIN = 2
    DASH = 3

    @staticmethod
    def get_items():
        return {
            CryptType.UNDEFINED: u'Не определен',
            CryptType.BITCOIN: u'Bitcoin',
            CryptType.LITECOIN: u'Litecoin',
            CryptType.DASH: u'Dash',
        }

    @staticmethod
    def get_item(item):
        return CryptType.get_items()[item]


class AlgorithmType:
    def __init__(self):
        pass

    UNDEFINED = 0
    SHA_256 = 1
    SCRYPT = 2
    X11 = 3

    @staticmethod
    def get_items():
        return {
            AlgorithmType.UNDEFINED: u'Не определен',
            AlgorithmType.SHA_256: u'SHA-256',
            AlgorithmType.SCRYPT: u'Scrypt',
            AlgorithmType.X11: u'X11',
        }

    @staticmethod
    def get_item(item):
        return AlgorithmType.get_items()[item]


class MeasureType:
    def __init__(self):
        pass

    MH_S = 0
    GH_S = 1
    TH_S = 2

    @staticmethod
    def convert(data, current_measure, new_measure):
        return data * 1000 ** (current_measure - new_measure)

    @staticmethod
    def get_items():
        return {
            MeasureType.MH_S: u'MH/S',
            MeasureType.GH_S: u'GH/S',
            MeasureType.TH_S: u'TH/S',
        }

    @staticmethod
    def get_item(item):
        return MeasureType.get_items()[item]


class ErrorLevel:
    def __init__(self):
        pass

    WARN = 1
    ERROR = 2

    @staticmethod
    def get_items():
        return {
            ErrorLevel.WARN: u'Предупреждение',
            ErrorLevel.ERROR: u'Ошибка',
        }

    @staticmethod
    def get_item(item):
        return ErrorLevel.get_items()[item]


class ErrorStatus:
    def __init__(self):
        pass

    OPEN = 1
    PENDING = 2
    NOT_SHOW = 3
    CLOSED = 4

    @staticmethod
    def get_items():
        return {
            ErrorStatus.OPEN: u'Открыта',
            ErrorStatus.PENDING: u'Ждет решения',
            ErrorStatus.NOT_SHOW: u'Не показывать',
            ErrorStatus.CLOSED: u'Закрыта',
        }

    @staticmethod
    def get_item(item):
        return ErrorStatus.get_items()[item]


class AsicTypeRate(models.Model):
    type = models.IntegerField(verbose_name=u'Тип ASIC', choices=AsicType.get_items().items(), null=False,
                               default=AsicType.UNDEFINED)
    default_rate = models.FloatField(verbose_name=u'Заявленная частота', default=0.0)
    measure = models.IntegerField(verbose_name=u'Мера', choices=MeasureType.get_items().items(),
                                  default=MeasureType.MH_S)

    class Meta:
        verbose_name = 'Заявленная частота ASIC'
        verbose_name_plural = 'Заявленные частоты ASIC'


class AsicQuerySet(models.QuerySet):
    def with_errors_and_warnings_count(self):
        errors = Subquery(
            Error.objects.filter(
                Q(level=ErrorLevel.ERROR) & Q(status__lt=ErrorStatus.CLOSED), asic=OuterRef('id')
            ).values('asic_id').annotate(cnt=Count('id'))
                .values('cnt')[:1],
            output_field=models.IntegerField())
        warnings = Subquery(
            Error.objects.filter(
                Q(level=ErrorLevel.WARN) & Q(status__lt=ErrorStatus.CLOSED), asic=OuterRef('id')
            ).values('asic_id').annotate(cnt=Count('id'))
                .values('cnt')[:1],
            output_field=models.IntegerField())
        connect_problems = Subquery(
            Error.objects.filter(
                Q(field_name=FieldName.CONNECT_ERROR) & Q(status__lt=ErrorStatus.CLOSED), asic=OuterRef('id')
            ).values('asic_id').annotate(cnt=Count('id'))
                .values('cnt')[:1],
            output_field=models.IntegerField()
        )

        return self.annotate(error_count=Coalesce(errors, 0), warning_count=Coalesce(warnings, 0), connect_problems=Coalesce(connect_problems, 0))

    def with_farm_name(self):
        return self.annotate(farm_name=F('farm__name'))

    def with_client_name(self):
        return self.annotate(client_name=F('client__name'))


class AsicManager(models.Manager):
    def get_queryset(self):
        return AsicQuerySet(self.model, using=self._db)

    def with_errors_and_warnings_count(self):
        return self.get_queryset().with_errors_and_warnings_count()

    def with_farm_name(self):
        return self.get_queryset().with_farm_name()

    def with_client_name(self):
        return self.get_queryset().with_client_name()


# asic:
#   type (s9 and so on)
#   mining_type (Bitcoin, Litecoin, Dash)
#   name
#   ip address
#   category
#   owner
#   metrics
#   default_capacity - заявленная мощность
#   parser usage: asic.parser.update()
class Asic(models.Model):
    farm = models.ForeignKey('Farm', verbose_name=u'Ферма', null=True, blank=True, on_delete=models.SET_NULL)

    type = models.IntegerField(verbose_name=u'Тип ASIC', choices=AsicType.get_items().items(), null=False,
                               default=AsicType.UNDEFINED)
    crypt_type = models.IntegerField(verbose_name=u'Вычисляемая валюта', choices=CryptType.get_items().items(),
                                     null=False, default=CryptType.UNDEFINED)
    alg_type = models.IntegerField(verbose_name=u'Алгоритм', choices=AlgorithmType.get_items().items(),
                                   null=False, default=AlgorithmType.UNDEFINED)
    name = models.CharField(verbose_name=u'Имя ASIC(необязательно)', max_length=100)
    ip_address = models.CharField(verbose_name=u'IP адрес ASIC', max_length=15)
    host_name = models.CharField(verbose_name=u'Имя хоста', max_length=100, null=True, blank=True)
    default_rate = models.FloatField(verbose_name=u'Заявленная частота', default=0.0)
    measure = models.IntegerField(verbose_name=u'Мера', choices=MeasureType.get_items().items(),
                                  default=MeasureType.MH_S)
    client = models.ForeignKey('Client', verbose_name=u'Клиент', null=True, blank=True, on_delete=models.SET_NULL)
    asic_name = models.CharField(max_length=100, verbose_name=u'Имя майнера', blank=True, null=True)
    pool_status = models.CharField(max_length=100, verbose_name=u'Статус пула', blank=True, null=True)
    full_rate = models.FloatField(verbose_name=u'Текущая мощность', default=0)
    pool_address = models.CharField(verbose_name=u'Адрес пула', blank=True, null=True, max_length=300)
    pool_username = models.CharField(verbose_name=u'Пользователь пула', blank=True, null=True, max_length=300)
    updated = models.DateTimeField(verbose_name=u'Обновлено', null=True)

    stop_update = models.BooleanField(verbose_name=u'Остановить обновление', default=False)
    resume_update_date = models.DateTimeField(verbose_name='Дата возобновления обновления', null=True)

    asic_info = models.OneToOneField(to='AsicInfo', verbose_name=u'Последняя информация об ASIC', blank=True, null=True,
                                     on_delete=models.SET_NULL,
                                     related_name='current_asic')
    username = models.CharField(max_length=100, verbose_name='Имя пользователя ASIC', blank=True, null=True)
    password = models.CharField(max_length=100, verbose_name='Пароль ASIC', blank=True, null=True)

    objects = AsicManager()

    def add_error(self, message, rule=None, object_id=None, field_name=''):
        try:
            self.errors.get(~Q(status=ErrorStatus.CLOSED), message=message, object_id=object_id)
        except Error.DoesNotExist:
            if rule is None:
                self.errors.create(message=message, field_name=field_name)
            else:
                if rule.error_rule is None:
                    self.errors.create(message=message, error_rule=rule,
                                       level=rule.error_level, object_id=object_id, field_name=rule.field_name)
                else:
                    try:
                        error = self.errors.get(~Q(status=ErrorStatus.CLOSED), error_rule=rule, object_id=object_id)
                        error.message = message
                        error.save()
                    except Error.DoesNotExist:
                        self.errors.create(message=message, error_rule=rule,
                                           level=rule.error_level, object_id=object_id, field_name=rule.field_name)
                    except Error.MultipleObjectsReturned:
                        if rule.error_level == ErrorLevel.ERROR:
                            self.errors.filter(~Q(status=ErrorStatus.CLOSED), error_rule=rule,
                                               object_id=object_id).delete()

                        self.errors.create(message=message, error_rule=rule, level=rule.error_level,
                                           object_id=object_id, field_name=rule.field_name)
        except Error.MultipleObjectsReturned:
            if rule.error_level == ErrorLevel.ERROR:
                self.errors.filter(~Q(status=ErrorStatus.CLOSED), error_rule=rule,
                                   object_id=object_id).delete()

            self.errors.create(message=message, error_rule=rule, level=rule.error_level,
                               object_id=object_id, field_name=rule.field_name)

    def has_connect_error(self):
        return self.errors.filter(~Q(status=ErrorStatus.CLOSED), level=ErrorLevel.ERROR,
                                  message__icontains='Проблемы с соединением').exists()

    def has_connect_warning(self):
        return self.errors.filter(~Q(status=ErrorStatus.CLOSED), level=ErrorLevel.WARN,
                                  message__icontains='Проблемы с соединением').exists()

    @cached_property
    def connect_error(self):
        return self.errors.filter(~Q(status=ErrorStatus.CLOSED), level=ErrorLevel.ERROR,
                                  message__icontains='Проблемы с соединением').first()

    @cached_property
    def connect_warning(self):
        return self.errors.filter(~Q(status=ErrorStatus.CLOSED), level=ErrorLevel.WARN,
                                  message__icontains='Проблемы с соединением').first()

    def down_level_connect_error(self):
        print('down level')
        if self.has_connect_warning():
            error = self.connect_warning
            error.status = ErrorStatus.CLOSED
            error.save()
        if self.has_connect_error():
            error = self.connect_error
            error.level = ErrorLevel.WARN
            error.save()

    def down_level_error(self, error_rule, object_id):
        # Если нет ворнинга три часа подряд, то закрываем ошибку
        date = (datetime.now() - timedelta(hours=3))

        errors = self.errors.filter(status=ErrorStatus.OPEN,
                                    error_rule=error_rule,
                                    level=ErrorLevel.WARN,
                                    object_id=object_id,
                                    created__lte=date)

        errors.update(status=ErrorStatus.CLOSED)

        # Если нет ошибки три часа подряд, то понижаем все предыдущие в ворнинг
        self.errors.filter(status=ErrorStatus.OPEN,
                           error_rule=error_rule,
                           level=ErrorLevel.ERROR,
                           object_id=object_id,
                           created__lte=date).update(level=ErrorLevel.WARN)

    @property
    def open_errors(self):
        return self.errors.filter(~Q(status=ErrorStatus.CLOSED), level=ErrorLevel.ERROR).order_by('-created').all()

    @property
    def open_warnings(self):
        return self.errors.filter(~Q(status=ErrorStatus.CLOSED), level=ErrorLevel.WARN).order_by('-created').all()

    @staticmethod
    def parser_map():
        from backend.parsers.a4plus_parsers import A4PlusParser
        from backend.parsers.d3_parsers import BaseD3Parser
        from backend.parsers.dr100_parsers import DR100Parser
        from backend.parsers.l21_parsers import L21Parser
        from backend.parsers.l3plus_parsers import L3PlusParser
        from backend.parsers.s9_parsers import S9Parser

        return {
            AsicType.S9: S9Parser,
            AsicType.L3PLUS: L3PlusParser,
            AsicType.DR100: DR100Parser,
            AsicType.A4PLUS: A4PlusParser,
            AsicType.L21: L21Parser,
            AsicType.D3: BaseD3Parser,
        }

    @property
    def parser(self):
        from backend.parsers.base_parser import UndefinedParser
        try:
            return self.__parser
        except AttributeError:
            try:
                self.__parser = Asic.parser_map()[self.type](self.ip_address, self.username, self.password)
            except KeyError:
                self.__parser = UndefinedParser(self.ip_address)

        return self.__parser

    @property
    def rate_is_lower(self):
        full_rate_converted = MeasureType.convert(self.asic_info.full_rate, self.asic_info.measure, self.measure)
        if full_rate_converted == 0:
            return False

        diff = (self.default_rate - full_rate_converted) / full_rate_converted * 100
        return True if diff >= 8 else False

    def update_info(self):
        info = self.parser.update(self)

        # info = AsicInfo(created=timezone.now(), changed=timezone.now(), json_data=json_data, asic=self)
        # info.save()

        return info

    def reboot(self):
        self.stop_update = True
        self.resume_update_date = datetime.now() + timedelta(hours=1)
        self.save()
        self.parser.reboot()

    def change_password(self, password):
        self.password = password
        self.save()
        self.parser.change_password(password)

    def __str__(self):
        return '{}:{} {}'.format(self.name, self.ip_address, AsicType.get_items()[self.type])

    class Meta:
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['type']),
            models.Index(fields=['alg_type']),
            models.Index(fields=['client']),
            models.Index(fields=['farm']),
            models.Index(fields=['asic_name']),
            models.Index(fields=['pool_status']),

            models.Index(fields=['client', 'pool_status']),
            models.Index(fields=['client', 'ip_address']),
            models.Index(fields=['client', 'type']),
            models.Index(fields=['client', 'alg_type']),
            models.Index(fields=['client', 'asic_name']),
            models.Index(fields=['client', 'farm']),
        ]


class AsicInfo(models.Model):
    created = models.DateTimeField(verbose_name=u'Создано')
    changed = models.DateTimeField(verbose_name=u'Изменено')
    asic = models.ForeignKey(Asic, verbose_name='ASIC', on_delete=models.CASCADE, related_name='asic_info_history')
    asic_name = models.CharField(max_length=100, verbose_name=u'Имя майнера', blank=True, null=True)
    host_name = models.CharField(max_length=100, verbose_name=u'Имя хоста', blank=True, null=True)
    pool_status = models.CharField(max_length=100, verbose_name=u'Статус пула', blank=True, null=True)
    full_rate = models.FloatField(verbose_name=u'Суммарная мощность', default=0)
    pool_address = models.CharField(verbose_name=u'Адрес пула', blank=True, null=True, max_length=300)
    pool_username = models.CharField(verbose_name=u'Пользователь пула', blank=True, null=True, max_length=300)

    class Meta:
        verbose_name = u'Информация об ASIC'
        verbose_name_plural = u'Информация об ASIC'
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return '{} {} {}'.format(self.asic, self.created, self.changed)

    @cached_property
    def full_rate_summ(self):
        return self.chain_info_set.aggregate(rate_sum=Sum('rate'))['rate_sum']

    @cached_property
    def measure(self):
        first_chain = self.chain_info_set.first()
        if first_chain is None:
            return MeasureType.MH_S
        else:
            return first_chain.measure

    @cached_property
    def measure_display(self):
        return MeasureType.get_items()[self.measure]


class JsonInfo(models.Model):
    json_data = JSONField(verbose_name=u'JSON данные')
    asic_info = models.OneToOneField(AsicInfo, on_delete=models.CASCADE, related_name='json_info')


class ChainInfo(models.Model):
    temperature = models.IntegerField(verbose_name=u'Температура')
    frequency = models.FloatField(verbose_name=u'Частота')
    rate = models.FloatField(verbose_name=u'Мощность')
    measure = models.IntegerField(verbose_name=u'Мера', choices=MeasureType.get_items().items(),
                                  default=MeasureType.MH_S)
    all_chips = models.IntegerField(verbose_name=u'Общее количество чипов', default=0)
    wrong_chips = models.IntegerField(verbose_name=u'Количество неработающих чипов', default=0)
    working_chips = models.IntegerField(verbose_name=u'Количество работающих чипов', default=0)
    asic = models.ForeignKey(Asic, related_name='chain_info_set', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = u'Информация по плате'
        verbose_name_plural = u'Данные по платам'

    @cached_property
    def success_percent(self):
        return self.working_chips / self.all_chips * 100 if self.all_chips else 0

    @cached_property
    def error_percent(self):
        return self.wrong_chips / self.all_chips * 100 if self.all_chips else 0


class FanInfo(models.Model):
    name = models.CharField(verbose_name=u'Наименование вентилятора', max_length=100)
    speed = models.IntegerField(verbose_name=u'Текущая скорость')
    asic = models.ForeignKey(Asic, related_name='fan_info_set', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = u'Данные по вентилятору'
        verbose_name_plural = u'Данные по вентиляторам'


class ValueType:
    def __init__(self):
        pass

    NUMBER = 0

    STRING = 1

    @staticmethod
    def get_items():
        return {
            ValueType.NUMBER: 'Числовое',
            ValueType.STRING: 'Строковое',
        }

    @staticmethod
    def get_item(item):
        return ValueType.get_items()[item]


class ComparisonType:
    def __init__(self):
        pass

    EQUAL = 0
    NOT_EQUAL = 1

    GREATER = 10
    GREATER_AND_EQUAL = 11
    LESSER = 12
    LESSER_AND_EQUAL = 13

    GREATER_PERCENT = 20
    GREATER_AND_EQUAL_PERCENT = 21
    LESSER_PERCENT = 22
    LESSER_AND_EQUAL_PERCENT = 23

    CONTAINS = 30
    NOT_CONTAINS = 31

    LESSER_THAN_WAS = 40
    GREATER_THAN_WAS = 41

    @staticmethod
    def get_items():
        return {
            ComparisonType.EQUAL: 'Равно',
            ComparisonType.NOT_EQUAL: 'Неравно',

            ComparisonType.GREATER: 'Больше (абсолютное)',
            ComparisonType.GREATER_AND_EQUAL: 'Больше или равно (абсолютное)',
            ComparisonType.LESSER: 'Меньше (абсолютное)',
            ComparisonType.LESSER_AND_EQUAL: 'Меньше или равно (абсолютное)',

            ComparisonType.GREATER_PERCENT: 'Больше (проценты)',
            ComparisonType.GREATER_AND_EQUAL_PERCENT: 'Больше или равно (проценты)',
            ComparisonType.LESSER_PERCENT: 'Меньше (проценты)',
            ComparisonType.LESSER_AND_EQUAL_PERCENT: 'Меньше или равно (проценты)',

            ComparisonType.LESSER_THAN_WAS: 'Меньше чем было на',
            ComparisonType.GREATER_THAN_WAS: 'Больше чем было на',

            ComparisonType.CONTAINS: 'Содержит (только для строковых)',
            ComparisonType.NOT_CONTAINS: 'Не содержит (только для строковых)',
        }

    @staticmethod
    def get_short_items():
        return {
            ComparisonType.EQUAL: '==',
            ComparisonType.NOT_EQUAL: '!=',

            ComparisonType.GREATER: '>',
            ComparisonType.GREATER_AND_EQUAL: '>=',
            ComparisonType.LESSER: '<',
            ComparisonType.LESSER_AND_EQUAL: '<=',

            ComparisonType.GREATER_PERCENT: '>',
            ComparisonType.GREATER_AND_EQUAL_PERCENT: '>=',
            ComparisonType.LESSER_PERCENT: '<',
            ComparisonType.LESSER_AND_EQUAL_PERCENT: '<=',

            ComparisonType.LESSER_THAN_WAS: '< на',
            ComparisonType.GREATER_THAN_WAS: '> на',

            ComparisonType.CONTAINS: 'Содержит',
            ComparisonType.NOT_CONTAINS: 'Не содержит',
        }

    @staticmethod
    def get_item(item):
        return ComparisonType.get_items()[item]


class FieldName:
    def __init__(self):
        pass

    CONNECT_ERROR = 'connect_error'

    ASIC_NAME = 'asic_name'
    HOST_NAME = 'host_name'
    POOL_STATUS = 'pool_status'
    FULL_RATE = 'full_rate'

    CHAIN_INFO_TEMPERATURE = 'chain_info_set__temperature'
    CHAIN_INFO_FREQUENCY = 'chain_info_set__frequency'
    CHAIN_INFO_RATE = 'chain_info_set__rate'
    CHAIN_INFO_ALL_CHIPS = 'chain_info_set__all_chips'
    CHAIN_INFO_WRONG_CHIPS = 'chain_info_set__wrong_chips'
    CHAIN_INFO_WORKING_CHIPS = 'chain_info_set__working_chips'

    FAN_INFO_NAME = 'fan_info_set__name'
    FAN_INFO_SPEED = 'fan_info_set__speed'

    ERROR_RULE_COUNT = 'error_rule_count'

    @staticmethod
    def get_items():
        return {
            FieldName.CONNECT_ERROR: u'Проблемы с подключением',
            FieldName.ASIC_NAME: u'Имя майнера',
            FieldName.HOST_NAME: u'Имя хоста',
            FieldName.POOL_STATUS: u'Статус пула',
            FieldName.FULL_RATE: u'Суммарная мощность',

            FieldName.CHAIN_INFO_TEMPERATURE: u'Температура на плате',
            FieldName.CHAIN_INFO_FREQUENCY: u'Частота платы',
            FieldName.CHAIN_INFO_RATE: u'Мощность платы',
            FieldName.CHAIN_INFO_ALL_CHIPS: u'Общее количество чипов на плате',
            FieldName.CHAIN_INFO_WRONG_CHIPS: u'Количество неработающих чипов на плате',
            FieldName.CHAIN_INFO_WORKING_CHIPS: u'Количество работающих чипов на плате',

            FieldName.FAN_INFO_NAME: u'Наименование вентилятора',
            FieldName.FAN_INFO_SPEED: u'Текущая скорость вентилятора',

            FieldName.ERROR_RULE_COUNT: u'Количество ошибок по правилу'
        }

    @staticmethod
    def get_short_items():
        return {
            FieldName.CONNECT_ERROR: u'Проблемы с подключением',
            FieldName.ASIC_NAME: u'Майнер',
            FieldName.HOST_NAME: u'Хост',
            FieldName.POOL_STATUS: u'Статус',
            FieldName.FULL_RATE: u'Сумм. мощ.',

            FieldName.CHAIN_INFO_TEMPERATURE: u'Темп. на плате',
            FieldName.CHAIN_INFO_FREQUENCY: u'Част. платы',
            FieldName.CHAIN_INFO_RATE: u'Мощ. платы',
            FieldName.CHAIN_INFO_ALL_CHIPS: u'Всего чипов на плате',
            FieldName.CHAIN_INFO_WRONG_CHIPS: u'Нераб. чипов на плате',
            FieldName.CHAIN_INFO_WORKING_CHIPS: u'Раб. чипов на плате',

            FieldName.FAN_INFO_NAME: u'Имя вент.',
            FieldName.FAN_INFO_SPEED: u'Скорость вент.',

            FieldName.ERROR_RULE_COUNT: u'Кол-во ошибок'
        }

    @staticmethod
    def get_item(item):
        return FieldName.get_items()[item]


class Error(models.Model):
    message = models.CharField(verbose_name=u'Сообщение об ошибке', max_length=3000)
    asic = models.ForeignKey(Asic, verbose_name=u'ASIC', null=True, related_name='errors', on_delete=models.SET_NULL)
    level = models.IntegerField(verbose_name=u'Уровень ошибки', choices=ErrorLevel.get_items().items(),
                                default=ErrorLevel.ERROR)
    status = models.IntegerField(verbose_name=u'Статус ошибки', choices=ErrorStatus.get_items().items(),
                                 default=ErrorStatus.OPEN)
    error_rule = models.ForeignKey('ErrorRule', verbose_name=u'Валидационное правило', null=True,
                                   on_delete=models.SET_NULL)
    field_name = models.CharField(verbose_name=u'Проверяемое значение', choices=FieldName.get_items().items(),
                                  null=False,
                                  default='', max_length=300)
    object_id = models.IntegerField(verbose_name=u'ИД объекта', null=True, blank=True)
    created = models.DateTimeField(verbose_name=u'Создана', default=timezone.now)

    class Meta:
        verbose_name = u'Ошибка'
        verbose_name_plural = u'Ошибки'
        indexes = [
            models.Index(fields=['level', 'status']),
            models.Index(fields=['level']),
            models.Index(fields=['status']),
            models.Index(fields=['error_rule']),
            models.Index(fields=['created']),
            models.Index(fields=['asic', 'level', 'status']),
        ]

    @staticmethod
    def get_current_errors():
        return Error.objects.filter(level=ErrorLevel.ERROR).filter(
            ~Q(status=ErrorStatus.CLOSED) & ~Q(status=ErrorStatus.NOT_SHOW))

    @staticmethod
    def get_current_warnings():
        return Error.objects.filter(level=ErrorLevel.WARN).filter(
            ~Q(status=ErrorStatus.CLOSED) & ~Q(status=ErrorStatus.NOT_SHOW))

    def get_history_errors(self):
        if self.error_rule is None:
            return []

        warning_rule = self.error_rule.error_rule

        if warning_rule is None:
            return []

        return self.asic.errors.filter(~Q(status=ErrorStatus.CLOSED), error_rule=warning_rule).all()


class ErrorRule(models.Model):
    asic_type = models.IntegerField(verbose_name=u'Тип ASIC', choices=AsicType.get_items().items(), null=False,
                                    default=AsicType.UNDEFINED)

    error_level = models.IntegerField(verbose_name=u'Уровень ошибки', choices=ErrorLevel.get_items().items(),
                                      default=ErrorLevel.WARN)

    error_rule = models.ForeignKey('self', verbose_name='Проверяемое правило', null=True, blank=True,
                                   on_delete=models.SET_NULL)

    field_name = models.CharField(verbose_name=u'Проверяемое значение', choices=FieldName.get_items().items(),
                                  null=False,
                                  default=FieldName.FULL_RATE, max_length=300)

    value_type = models.IntegerField(verbose_name=u'Тип значения', choices=ValueType.get_items().items(), null=False,
                                     default=ValueType.NUMBER)
    comparison_type = models.IntegerField(verbose_name=u'Сравнение', choices=ComparisonType.get_items().items(),
                                          null=False,
                                          default=ComparisonType.EQUAL)
    value = models.CharField(verbose_name=u'Значение', max_length=100)
    percent = models.IntegerField(verbose_name=u'Процент', null=True, default=None, blank=True)

    message = models.CharField(verbose_name=u'Сообщение об ошибке', max_length=3000, blank=True, null=True)

    # Привязка к типу асика = например, только для д3 или для всех
    # числовое значение\строковое значение
    # больше или равно, содержит и тд
    # наименование поля - choices из лейблов и внутренних наименований полей

    class Meta:
        verbose_name = 'Валидационное правило'
        verbose_name_plural = 'Валидационные правила'

    @staticmethod
    def get_func_map(rule):
        value = rule.value
        field_name = rule.field_name
        percent = rule.percent
        message = rule.message

        if field_name == FieldName.ERROR_RULE_COUNT:
            format_error_message = '{} Текущее значение: {} циклов обновлений. Требуемое значение: {} циклов обновлений'
        else:
            format_error_message = '{} Текущее значение: {}. Требуемое значение: {}'

        def get_value(asic_info, name):
            if name == FieldName.ERROR_RULE_COUNT:
                return asic_info.errors.filter(
                    ~Q(status=ErrorStatus.CLOSED) & ~Q(status=ErrorStatus.NOT_SHOW), error_rule=rule.error_rule,
                    level=ErrorLevel.WARN).count()

            return getattr(asic_info, name)

        def base_func(asic_info, check_func):

            result = []
            if asic_info is None:
                result.append([True, '{} Невозможно получить данные'.format(message)])

            fields = field_name.split('__')
            if len(fields) == 1:
                result.append([
                    check_func(asic_info, fields[0]), format_error_message.format(
                        message, get_value(asic_info, fields[0]), value)
                ])
            else:
                set = get_value(asic_info, fields[0])
                for item in set.all():
                    if check_func(item, fields[1]):
                        result.append(
                            [True, format_error_message.format(message, get_value(item, fields[1]), value), item.pk])
                    else:
                        result.append(
                            [False, format_error_message.format(message, get_value(item, fields[1]), value), item.pk])
            return result

        def equal_number_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) == float(value))

        def not_equal_number_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) != float(value))

        def equal_string_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) == value)

        def not_equal_string_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) != value)

        def contains_func(asic_info):
            return base_func(asic_info, lambda x, attr: value in get_value(x, attr))

        def not_contains_func(asic_info):
            return base_func(asic_info, lambda x, attr: value not in get_value(x, attr))

        def greater_abs_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) > float(value))

        def greater_and_equal_abs_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) >= float(value))

        def lesser_abs_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) < float(value))

        def lesser_and_equal_abs_func(asic_info):
            return base_func(asic_info, lambda x, attr: get_value(x, attr) <= float(value))

        def greater_percent_func(asic_info):
            return base_func(asic_info,
                             lambda x, attr: (get_value(x, attr) - float(value)) / float(value) * 100 > percent)

        def greater_and_equal_percent_func(asic_info):
            return base_func(asic_info,
                             lambda x, attr: (get_value(x, attr) - float(value)) / float(value) * 100 >= percent)

        def lesser_percent_func(asic_info):
            return base_func(asic_info,
                             lambda x, attr: (get_value(x, attr) - float(value)) / float(value) * 100 < percent)

        def lesser_and_equal_percent_func(asic_info):
            return base_func(asic_info,
                             lambda x, attr: (get_value(x, attr) - float(value)) / float(value) * 100 <= percent)

        def base_behind_compare_func(asic_info, check_func):
            if asic_info is None:
                return [
                    [True, '{} Невозможно получить данные'.format(message)]
                ]

            try:
                prev_asic_info = asic_info.asic.asic_info_history[::-2][-1]
            except IndexError:
                return [
                    [False, '']
                ]

            fields = field_name.split('__')
            if len(fields) == 1:
                return [
                    [
                        check_func(asic_info, prev_asic_info, fields[0]), \
                        format_error_message.format(message, getattr(asic_info, fields[0]),
                                                    get_value(prev_asic_info, fields[0]))
                    ]]

            set1 = get_value(asic_info, fields[0])
            set2 = get_value(prev_asic_info, fields[0])
            return [[check_func(set1, set2, fields[1], True), \
                     format_error_message.format(message, get_value(set1, fields[0]), get_value(set1, fields[0]))]]

        def lesser_than_was_func(asic_info):
            return base_behind_compare_func(asic_info, lambda x, prev, attr, is_func=True:
            get_value(x, attr)() - get_value(prev, attr)() > float(value) if is_func
            else get_value(x, attr) - get_value(prev, attr) > float(value)
                                            )

        def greater_than_was_func(asic_info):
            return base_behind_compare_func(asic_info, lambda x, prev, attr, is_func=True:
            get_value(x, attr)() - get_value(prev, attr)() < float(value) if is_func
            else get_value(x, attr) - get_value(prev, attr) < float(value)
                                            )

        return {
            ValueType.NUMBER: {
                ComparisonType.EQUAL: equal_number_func,
                ComparisonType.NOT_EQUAL: not_equal_number_func,

                ComparisonType.GREATER: greater_abs_func,
                ComparisonType.GREATER_AND_EQUAL: greater_and_equal_abs_func,
                ComparisonType.LESSER: lesser_abs_func,
                ComparisonType.LESSER_AND_EQUAL: lesser_and_equal_abs_func,

                ComparisonType.GREATER_PERCENT: greater_percent_func,
                ComparisonType.GREATER_AND_EQUAL_PERCENT: greater_and_equal_percent_func,
                ComparisonType.LESSER_PERCENT: lesser_percent_func,
                ComparisonType.LESSER_AND_EQUAL_PERCENT: lesser_and_equal_percent_func,

                ComparisonType.LESSER_THAN_WAS: lesser_than_was_func,
                ComparisonType.GREATER_THAN_WAS: greater_than_was_func
            },
            ValueType.STRING: {
                ComparisonType.EQUAL: equal_string_func,
                ComparisonType.NOT_EQUAL: not_equal_string_func,
                ComparisonType.CONTAINS: contains_func,
                ComparisonType.NOT_CONTAINS: not_contains_func,
            }
        }

    def convert_to_func(self):
        return ErrorRule.get_func_map(self)[self.value_type][self.comparison_type]

    def get_enum_field_with_verbose_name(self, field, enum_type):
        return '{}: {}.'.format(ErrorRule._meta.get_field(field).verbose_name, enum_type.get_item(getattr(self, field)))

    def get_field_with_verbose_name(self, field):
        return '{}: {}.'.format(ErrorRule._meta.get_field(field).verbose_name, getattr(self, field))

    def get_short_string(self):
        percent_operations = [
            ComparisonType.GREATER_PERCENT,
            ComparisonType.GREATER_AND_EQUAL_PERCENT,
            ComparisonType.LESSER_PERCENT,
            ComparisonType.LESSER_AND_EQUAL_PERCENT,
        ]

        if self.comparison_type not in percent_operations and self.field_name != FieldName.ERROR_RULE_COUNT:
            return '{} {} {}'.format(
                FieldName.get_short_items()[self.field_name],
                ComparisonType.get_short_items()[self.comparison_type],
                self.value
            )

        if self.comparison_type in percent_operations and self.field_name != FieldName.ERROR_RULE_COUNT:
            return '{} {} {} ({}%)'.format(
                FieldName.get_short_items()[self.field_name],
                ComparisonType.get_short_items()[self.comparison_type],
                self.value,
                self.percent
            )

        if self.comparison_type not in percent_operations and self.field_name == FieldName.ERROR_RULE_COUNT:
            return '{} {} {}'.format(
                FieldName.get_short_items()[self.field_name],
                ComparisonType.get_short_items()[self.comparison_type],
                self.value
            )

        return ''

    def __str__(self):
        asic_type = self.get_enum_field_with_verbose_name('asic_type', AsicType)
        error_level = self.get_enum_field_with_verbose_name('error_level', ErrorLevel)
        field_name = self.get_enum_field_with_verbose_name('field_name', FieldName)
        value_type = self.get_enum_field_with_verbose_name('value_type', ValueType)
        comparison_type = self.get_enum_field_with_verbose_name('comparison_type', ComparisonType)

        value = self.get_field_with_verbose_name('value')
        percent = self.get_field_with_verbose_name('percent')

        result = '{} {} {} {} {} {} {}'.format(asic_type, error_level, field_name, value_type, comparison_type, value,
                                               percent)

        return result


class Farm(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Имя фермы')

    class Meta:
        verbose_name = u'Ферма'
        verbose_name_plural = u'Фермы'
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Имя клиента')

    class Meta:
        verbose_name = u'Клиент'
        verbose_name_plural = u'Клиенты'
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class Subnet(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Имя подсети')
    masks = models.CharField(max_length=1000, verbose_name=u'Маски подсетей')
    exclude_ips = models.CharField(max_length=10000, verbose_name=u'IP для исключения', null=True, blank=True)

    class Meta:
        verbose_name = u'Подсеть'
        verbose_name_plural = u'Подсети'

    def __str__(self):
        return self.name


class Counter(models.Model):
    name = models.CharField(max_length=30, verbose_name='Наименование')
    value = models.FloatField(verbose_name='Значение', null=True, default=0)
    preliminary_tariff = models.FloatField(verbose_name='Предварительный тариф', null=True, default=0)
    approved_tariff = models.FloatField(verbose_name='Подтвержденный тариф', null=True, default=0)
    koefficient = models.FloatField(verbose_name='Коэффициент', null=True, default=0)
    counter_record = models.ForeignKey('CounterRecord', related_name='counters', verbose_name='Запись данных',
                                       on_delete=models.CASCADE)


class CounterRecord(models.Model):
    date = models.DateField(verbose_name='Дата')

# metrics:
#   name (Bitcoin, LiteCoin, Dash, etc)
#   measure (MH, GH, TH)
#

# category:
#   name

# parsers - каждый парсер выбирается в зависимости от типа асика и от того, что он майнит - потому что разные метрики
