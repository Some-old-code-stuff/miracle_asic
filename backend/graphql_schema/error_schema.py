# -*- coding: utf-8 -*-
import graphene
from django.db.models import Q
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

import backend.common.models as models
from backend.graphql_schema.fields import ErrorStatusMutation, ErrorLevelMutation


class ErrorObjectType(DjangoObjectType):
    field_name = graphene.String()
    error_rule_id = graphene.Int()
    warning_rule_id = graphene.Int()
    created = graphene.String()
    status = graphene.String()
    status_value = graphene.Int()
    level = graphene.String()
    level_value = graphene.Int()
    asic_id = graphene.Int()

    class Meta:
        model = models.Error

    def resolve_field_name(self, info):
        return self.field_name

    def resolve_error_rule_id(self, info):
        return self.error_rule_id

    def resolve_warning_rule_id(self, info):
        if self.error_rule_id is None:
            return None

        return self.error_rule.error_rule_id

    def resolve_created(instance, info):
        try:
            created = timezone.localtime(instance.created)
        except ValueError:
            created = instance.created
        return "{:%d.%m.%Y %H:%M:%S}".format(created)

    def resolve_status(instance, info):
        return instance.get_status_display()

    def resolve_status_value(instance, info):
        return instance.status

    def resolve_level(instance, info):
        return instance.get_level_display()

    def resolve_level_value(instance, info):
        return instance.level

    def resolve_asic_id(instance, info):
        return instance.asic_id


class ErrorQuery(object):
    open_errors = graphene.List(ErrorObjectType, asic_id=graphene.Int())
    open_warnings = graphene.List(ErrorObjectType, asic_id=graphene.Int())
    errors = graphene.List(ErrorObjectType, asic_id=graphene.Int(), level=graphene.Int(), closed=graphene.Boolean())

    @staticmethod
    @login_required
    def resolve_errors(self, info, **kwargs):
        asic_id = kwargs.get('asic_id')
        level = kwargs.get('level')
        closed = kwargs.get('closed')
        # if level is None:
        #     level = models.ErrorLevel.ERROR
        if closed is None:
            closed = False
        result = models.Error.objects
        if not closed:
            result = result.filter(~Q(status=models.ErrorStatus.CLOSED))

        if level is not None:
            result = result.filter(level=level)
        if asic_id is not None:
            result = result.filter(asic_id=asic_id)
        return result.order_by('-created').all()

    @staticmethod
    @login_required
    def resolve_open_errors(self, info, **kwargs):
        kwargs['level'] = models.ErrorLevel.ERROR
        return ErrorQuery.resolve_errors(self, info, **kwargs)

    @staticmethod
    @login_required
    def resolve_open_warnings(self, info, **kwargs):
        kwargs['level'] = models.ErrorLevel.WARN
        return ErrorQuery.resolve_errors(self, info, **kwargs)


class ToPending(ErrorStatusMutation, graphene.Mutation):
    @login_required
    def mutate(self, info, error_id):
        return ToPending.change_status(error_id, models.ErrorStatus.PENDING, ToPending)


class CloseError(ErrorStatusMutation, graphene.Mutation):
    @login_required
    def mutate(self, info, error_id):
        return CloseError.change_status(error_id, models.ErrorStatus.CLOSED, CloseError)


class ToError(ErrorLevelMutation, graphene.Mutation):
    @login_required
    def mutate(self, info, error_id):
        return ToError.change_level(error_id, models.ErrorLevel.ERROR, ToError)


class ToWarning(ErrorLevelMutation, graphene.Mutation):
    @login_required
    def mutate(self, info, error_id):
        return ToWarning.change_level(error_id, models.ErrorLevel.WARN, ToWarning)


class ErrorMutations(object):
    to_pending = ToPending.Field()
    close_error = CloseError.Field()
    to_error = ToError.Field()
    to_warning = ToWarning.Field()
