# -*- coding: utf-8 -*-
import graphene

from backend.common import models


class OkField(graphene.ObjectType):
    ok = graphene.Boolean()


class AsicMutation(OkField):
    class Arguments:
        asic_id = graphene.NonNull(graphene.Int)


class ErrorMutation(OkField):
    class Arguments:
        error_id = graphene.NonNull(graphene.Int)


class ErrorStatusMutation(ErrorMutation):
    status = graphene.String()
    status_value = graphene.Int()

    @staticmethod
    def change_status(error_id, status, result_class):
        try:
            error = models.Error.objects.get(pk=error_id)
            error.status = status
            error.save()
            return result_class(status=error.get_status_display(), status_value=error.status, ok=True)
        except models.Error.DoesNotExist:
            return result_class(ok=False)


class ErrorLevelMutation(ErrorMutation):
    asic_id = graphene.Int()

    @staticmethod
    def change_level(error_id, level, result_class):
        try:
            error = models.Error.objects.get(pk=error_id)
            error.level = level
            error.save()
            return result_class(asic_id=error.asic_id, ok=True)
        except models.Error.DoesNotExist:
            return result_class(ok=False)


class EnumObjectType(graphene.ObjectType):
    value = graphene.String()
    text = graphene.String()

    def resolve_value(self, info):
        try:
            return self[0]
        except KeyError:
            return self['value']

    def resolve_text(self, info):
        print(self, info)
        try:
            return self[1]
        except KeyError:
            return self['text']