# -*- coding: utf-8 -*-
import graphene
from graphene_django import DjangoObjectType
import backend.common.models as models
from backend.graphql_schema.fields import OkField
import decimal


class CounterObjectType(DjangoObjectType):
    test_tariff = graphene.Float()

    class Meta:
        model = models.Counter

    def resolve_test_tariff(self, info):
        return round(decimal.Decimal(self.approved_tariff + 0.4), 2)


class CounterRecordObjectType(DjangoObjectType):
    class Meta:
        model = models.CounterRecord

    def resolve_counters(self, info):
        return self.counters.order_by('id')


class BalanceQuery(object):
    get_balance = graphene.List(CounterRecordObjectType)

    def resolve_get_balance(self, info):
        return models.CounterRecord.objects.prefetch_related('counters').order_by('date').all()[1:]


class AddCounterRecord(graphene.Mutation, OkField):
    id = graphene.Int()

    class Arguments:
        date = graphene.Date()

    def mutate(self, info, date):
        result = models.CounterRecord(date=date)
        result.save()
        previous = models.CounterRecord.objects.order_by('-date').filter(date__lt=date).first()

        for counter in previous.counters.all():
            result.counters.create(koefficient=counter.koefficient, name=counter.name, preliminary_tariff=counter.approved_tariff)
        # result.counters.create(koefficient=80, name='Счетчик 2', preliminary_tariff=previous_tariff)
        # result.counters.create(koefficient=80, name='Счетчик 3', preliminary_tariff=previous_tariff)
        return AddCounterRecord(ok=True, id=result.id)


class DeleteCounterRecord(graphene.Mutation, OkField):
    class Arguments:
        record_id = graphene.NonNull(graphene.Int)

    def mutate(self, info, record_id):
        try:
            models.CounterRecord.objects.get(pk=record_id).delete()
            return DeleteCounterRecord(ok=True)
        except models.CounterRecord.DoesNotExist:
            return DeleteCounterRecord(ok=False)


class AddCounter(graphene.Mutation, OkField):
    id = graphene.Int()

    class Arguments:
        record_id = graphene.NonNull(graphene.Int)
        name = graphene.String()
        value = graphene.Float()
        preliminary_tariff = graphene.Float()
        approved_tariff = graphene.Float()
        koefficient = graphene.Float()

    def mutate(self, info, record_id, name, value, preliminary_tariff, approved_tariff, koefficient):
        result = models.Counter(
            name=name,
            value=value,
            preliminary_tariff=preliminary_tariff,
            approved_tariff=approved_tariff,
            koefficient=koefficient,
            counter_record_id=record_id
        )
        result.save()
        return AddCounterRecord(ok=True, id=result.id)


class UpdateCounter(graphene.Mutation, OkField):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        value = graphene.Float()
        preliminary_tariff = graphene.Float()
        approved_tariff = graphene.Float()
        koefficient = graphene.Float()

    def mutate(self, info, id, name, value, preliminary_tariff, approved_tariff, koefficient):
        models.Counter.objects.filter(id=id).update(
            name=name,
            value=value,
            preliminary_tariff=preliminary_tariff,
            approved_tariff=approved_tariff,
            koefficient=koefficient
        )

        return AddCounterRecord(ok=True)


class DeleteCounter(graphene.Mutation, OkField):
    class Arguments:
        counter_id = graphene.NonNull(graphene.Int)

    def mutate(self, info, counter_id):
        try:
            models.Counter.objects.get(pk=counter_id).delete()
            return DeleteCounter(ok=True)
        except models.Counter.DoesNotExist:
            return DeleteCounter(ok=False)


class BalanceMutations(object):
    add_counter_record = AddCounterRecord.Field()
    delete_counter_record = DeleteCounterRecord.Field()
    add_counter = AddCounter.Field()
    update_counter = UpdateCounter.Field()
    delete_counter = DeleteCounter.Field()
