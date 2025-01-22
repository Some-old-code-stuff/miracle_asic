# -*- coding: utf-8 -*-
import graphene
from django.db.models import F
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from backend.common import models
from backend.graphql_schema.fields import EnumObjectType, OkField


class ErrorRuleEdit(DjangoObjectType):
    asic_type = graphene.Int()
    error_level = graphene.Int()
    field_name = graphene.String()
    value_type = graphene.Int()
    comparison_type = graphene.Int()
    error_rule = graphene.Int()

    class Meta:
        model = models.ErrorRule

    def resolve_error_rule(self, info):
        return self.error_rule_id


class ErrorRuleTable(DjangoObjectType):
    asic_type = graphene.String()
    error_level = graphene.String()
    error_level_value = graphene.Int()
    field_name = graphene.String()
    value_type = graphene.String()
    comparison_type = graphene.String()
    short_string = graphene.String()

    class Meta:
        model = models.ErrorRule

    def resolve_asic_type(instance, info):
        result = instance.get_asic_type_display()

        if result == models.AsicType.get_item(models.AsicType.UNDEFINED):
            return 'Общее правило'

        return result

    def resolve_error_level_value(self, info):
        return self.error_level

    def resolve_error_level(instance, info):
        return instance.get_error_level_display()

    def resolve_field_name(instance, info):
        return instance.get_field_name_display()

    def resolve_value_type(instance, info):
        return instance.get_value_type_display()

    def resolve_comparison_type(instance, info):
        return instance.get_comparison_type_display()

    def resolve_short_string(instance, info):
        return instance.get_short_string()


class ErrorRuleQuery(object):
    error_rules = graphene.List(ErrorRuleTable,
                                asic_type=graphene.Int())
    error_rule = graphene.Field(ErrorRuleEdit, id=graphene.Int())
    error_rule_error_levels = graphene.List(EnumObjectType)
    error_rule_field_names = graphene.List(EnumObjectType)
    error_rule_asic_types = graphene.List(EnumObjectType)
    error_rules_short = graphene.List(EnumObjectType)

    @staticmethod
    def resolve_enum(items, all_name=None):
        items = list(items)
        if all_name is None:
            return items

        return [(None, all_name)] + items

    @login_required
    def resolve_error_rule_error_levels(self, info, **kwargs):
        return models.ErrorLevel.get_items().items()

    @login_required
    def resolve_error_rule_field_names(self, info, **kwargs):
        return models.FieldName.get_items().items()

    @login_required
    def resolve_error_rule_asic_types(self, info, **kwargs):
        return models.AsicType.get_items().items()

    @login_required
    def resolve_error_rules(self, info, asic_type=None, **kwargs):
        queryset = models.ErrorRule.objects.select_related('error_rule').all()

        if asic_type is not None:
            queryset = queryset.filter(asic_type=asic_type)

        return queryset.order_by('asic_type', 'value_type')

    @login_required
    def resolve_error_rule(self, info, id):
        return models.ErrorRule.objects.get(pk=id)

    @login_required
    def resolve_error_rules_short(self, info):
        items = models.ErrorRule.objects.filter(error_rule=None).all()
        items = [{'value': x.id, 'text': x.get_short_string()} for x in items]
        return ErrorRuleQuery.resolve_enum(items, 'Без доп.правила')


class AddErrorRule(graphene.Mutation, OkField):
    class Arguments:
        asic_type = graphene.Int()
        error_level = graphene.Int()
        field_name = graphene.String()
        error_rule = graphene.Int()
        value_type = graphene.Int()
        comparison_type = graphene.Int()
        value = graphene.String()
        percent = graphene.Int()
        message = graphene.String()

    @login_required
    def mutate(self, info, asic_type, error_level, field_name, value_type, comparison_type, value,
               message, percent=None, error_rule=None):
        rule = models.ErrorRule(
            asic_type=asic_type,
            error_level=error_level,
            field_name=field_name,
            error_rule_id=error_rule,
            value_type=value_type,
            comparison_type=comparison_type,
            value=value,
            percent=percent,
            message=message,
        )
        rule.save()
        return AddErrorRule(ok=True)


class UpdateErrorRule(graphene.Mutation, OkField):
    class Arguments:
        id = graphene.Int()
        asic_type = graphene.Int()
        error_level = graphene.Int()
        field_name = graphene.String()
        error_rule = graphene.Int()
        value_type = graphene.Int()
        comparison_type = graphene.Int()
        value = graphene.String()
        percent = graphene.Int()
        message = graphene.String()

    @login_required
    def mutate(self, info, id, asic_type, error_level, field_name, value_type, comparison_type, value,
               message, percent=None, error_rule=None):
        models.ErrorRule.objects.filter(pk=id).update(
            asic_type=asic_type,
            error_level=error_level,
            field_name=field_name,
            error_rule=error_rule,
            value_type=value_type,
            comparison_type=comparison_type,
            value=value,
            percent=percent,
            message=message,
        )
        return UpdateErrorRule(ok=True)


class DeleteErrorRule(graphene.Mutation, OkField):
    class Arguments:
        error_rule_id = graphene.Int()

    @login_required
    def mutate(self, info, error_rule_id):
        models.ErrorRule.objects.filter(pk=error_rule_id).delete()
        return DeleteErrorRule(ok=True)


class ErrorRuleMutations(object):
    add_error_rule = AddErrorRule.Field()
    update_error_rule = UpdateErrorRule.Field()
    delete_error_rule = DeleteErrorRule.Field()
    pass
