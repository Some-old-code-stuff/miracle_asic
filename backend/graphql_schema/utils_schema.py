# -*- coding: utf-8 -*-

import graphene
from django.conf import settings
from django.db.models import F
from django.db.models import Q
from graphql_jwt.decorators import login_required

import backend.common.models as models
from backend.graphql_schema.fields import EnumObjectType


class Object(object):
    pass



class MenuInfoObjectType(graphene.ObjectType):
    asic_count = graphene.Int()
    error_asic_count = graphene.Int()
    error_count = graphene.Int()
    warning_count = graphene.Int()
    flower_url = graphene.String()
    admin_url = graphene.String()


class UtilsQuery(object):
    error_levels = graphene.List(EnumObjectType)
    field_names = graphene.List(EnumObjectType)
    asic_types = graphene.List(EnumObjectType)
    alg_types = graphene.List(EnumObjectType)
    value_types = graphene.List(EnumObjectType)
    comparison_types = graphene.List(EnumObjectType)
    error_rules_short = graphene.List(EnumObjectType)
    farms = graphene.List(EnumObjectType)
    clients = graphene.List(EnumObjectType)
    menu_info = graphene.Field(MenuInfoObjectType)

    @staticmethod
    def resolve_enum(items, all_name=None):
        items = list(items)
        if all_name is None:
            return items

        return [(None, all_name)] + items

    @login_required
    def resolve_error_levels(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.ErrorLevel.get_items().items(), 'Любой уровень')

    @login_required
    def resolve_field_names(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.FieldName.get_items().items(), 'Любое значение')

    @login_required
    def resolve_asic_types(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.AsicType.get_items().items(), 'Любой тип')

    @login_required
    def resolve_alg_types(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.AlgorithmType.get_items().items(), 'Любой алгоритм')

    @login_required
    def resolve_value_types(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.ValueType.get_items().items())

    @login_required
    def resolve_comparison_types(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.ComparisonType.get_items().items())

    @login_required
    def resolve_value_types(self, info, **kwargs):
        return UtilsQuery.resolve_enum(models.ValueType.get_items().items())

    @login_required
    def resolve_farms(self, info, **kwargs):
        items = models.Farm.objects.annotate(value=F('id'), text=F('name')).values('value', 'text').all()
        return UtilsQuery.resolve_enum(items, 'Любая ферма')

    @login_required
    def resolve_clients(self, info, **kwargs):
        items = models.Client.objects.annotate(value=F('id'), text=F('name')).values('value', 'text').all()
        return UtilsQuery.resolve_enum(items, 'Любой клиент')

    @login_required
    def resolve_menu_info(self, info):
        result = Object()
        result.asic_count = models.Asic.objects.count()
        result.error_asic_count = models.Asic.objects.with_errors_and_warnings_count() \
            .filter(Q(error_count__gt=0) & Q(connect_problems=0)).count()
        result.warning_asic_count = models.Asic.objects.with_errors_and_warnings_count() \
            .filter(Q(warning_count__gt=0, error_count=0), connect_problems=0).count()
        result.disconnected_asic_count = models.Asic.objects.with_errors_and_warnings_count().filter(connect_problems__gt=0)
        result.flower_url = settings.FLOWER_URL
        result.admin_url = settings.ADMIN_URL

        return result