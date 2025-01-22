# -*- coding: utf-8 -*-

import graphene
from django.db.models import Count, IntegerField, OuterRef, Q, Subquery
from django.db.models import Prefetch
from django.db.models.functions import Coalesce
from django.utils import timezone
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

import backend.common.models as models
from backend.common import tasks
from backend.graphql_schema.error_schema import ErrorObjectType
import backend.graphql_schema.fields as fields


class FarmObjectType(DjangoObjectType):
    class Meta:
        model = models.Farm


class ClientObjectType(DjangoObjectType):
    class Meta:
        model = models.Client


class ChainInfoObjectType(DjangoObjectType):
    measure = graphene.String()
    rate = graphene.String()

    class Meta:
        model = models.ChainInfo

    def resolve_measure(self, info, **kwargs):
        return self.get_measure_display()

    def resolve_rate(instance, info, **kwargs):
        return "{:.2f} {}".format(instance.rate, instance.get_measure_display())


class FanInfoObjectType(DjangoObjectType):
    class Meta:
        model = models.FanInfo


class AsicObjectType(DjangoObjectType):
    farm_name = graphene.String()
    client_name = graphene.String()
    type = graphene.String()
    alg_type = graphene.String()
    measure = graphene.String()
    chains = graphene.List(ChainInfoObjectType)
    fans = graphene.List(FanInfoObjectType)
    full_rate = graphene.String()
    default_rate = graphene.String()
    updated = graphene.String()

    class Meta:
        model = models.Asic

    def resolve_farm_name(instance, info, **kwargs):
        if instance.farm_name is None or instance.farm_name == '':
            return 'Не указано'

        return instance.farm_name

    def resolve_client_name(instance, info, **kwargs):
        if instance.client_name is None or instance.client_name == '':
            return 'Не указано'
        return instance.client_name

    def resolve_type(instance, info, **kwargs):
        return instance.get_type_display()

    def resolve_alg_type(instance, info, **kwargs):
        return instance.get_alg_type_display()

    def resolve_measure(instance, info, **kwargs):
        return instance.get_measure_display()

    def resolve_full_rate(instance, info, **kwargs):
        return "{:.2f} {}".format(instance.full_rate, instance.get_measure_display())

    def resolve_default_rate(instance, info, **kwargs):
        return "{:.2f} {}".format(instance.default_rate, instance.get_measure_display())

    def resolve_updated(instance, info, **kwargs):
        if instance.updated is None:
            return 'Не обновлялся'
        try:
            updated = timezone.localtime(instance.updated)
        except ValueError:
            updated = instance.updated
        return "{:%d.%m %H:%M:%S}".format(updated)


class AsicConnection(graphene.Connection):
    class Meta:
        node = AsicObjectType


class AsicSettings(graphene.ObjectType):
    username = graphene.String()
    password = graphene.String()


class AsicQuery(object):
    search_asics = graphene.List(
        AsicObjectType,
        asic_type=graphene.Int(),
        alg_type=graphene.Int(),
        farm=graphene.Int(),
        client=graphene.Int(),
        asic_name=graphene.String(),
        ip_address=graphene.String(),
        pool_status=graphene.String(),
        farm_name=graphene.String(),
        client_name=graphene.String(),
        error_level=graphene.Int(),
        field_name=graphene.String(),
        with_disabled_autoupdate=graphene.Boolean(),
        with_connection_errors=graphene.Boolean(),
        with_errors=graphene.Boolean(),
        with_warnings=graphene.Boolean(),
        unregistered_asics=graphene.Boolean(),
    )
    asic_errors = graphene.List(ErrorObjectType, asic_id=graphene.Int(), field_name=graphene.String(),
                                object_id=graphene.Int())
    dashboard_asics = graphene.ConnectionField(AsicConnection)
    asic_settings = graphene.Field(AsicSettings, asic_id=graphene.Int())

    # @login_required
    def resolve_search_asics(self, info, **kwargs):
        asic_type = kwargs.get('asic_type')
        alg_type = kwargs.get('alg_type')
        farm = kwargs.get('farm')
        client = kwargs.get('client')
        asic_name = kwargs.get('asic_name')
        ip_address = kwargs.get('ip_address')
        pool_status = kwargs.get('pool_status')
        client_name = kwargs.get('client_name')
        farm_name = kwargs.get('farm_name')
        error_level = kwargs.get('error_level')
        field_name = kwargs.get('field_name')
        with_disabled_autoupdate = kwargs.get('with_disabled_autoupdate', False)
        with_connection_errors = kwargs.get('with_connection_errors', False)
        with_errors = kwargs.get('with_errors', False)
        with_warnings = kwargs.get('with_warnings', False)
        unregistered_asics = kwargs.get('unregistered_asics', False)

        errors = models.Error.objects.filter(status__lt=models.ErrorStatus.CLOSED) \
            .order_by('asic_id', 'field_name', 'level', 'object_id', '-created') \
            .distinct('asic_id', 'field_name', 'level', 'object_id')
        qs = models.Asic.objects
        if asic_type is not None:
            qs = qs.filter(type=asic_type)
        if alg_type is not None:
            qs = qs.filter(alg_type=alg_type)
        if farm is not None:
            qs = qs.filter(farm=farm)
        if client is not None:
            qs = qs.filter(client=client)
        if asic_name is not None:
            qs = qs.filter(asic_name__icontains=asic_name)
        if ip_address is not None:
            qs = qs.filter(ip_address__icontains=ip_address)
        if pool_status is not None:
            qs = qs.filter(pool_status__icontains=pool_status)
        if client_name is not None:
            qs = qs.filter(client__name__icontains=client_name)
        if farm_name is not None:
            qs = qs.filter(farm__name__icontains=farm_name)

        if error_level is not None or field_name is not None:
            error_subquery = models.Error.objects.filter(status__lt=models.ErrorStatus.CLOSED, asic=OuterRef('id'))

            if error_level is not None and error_level != '':
                error_subquery = error_subquery.filter(level=error_level)
            if field_name is not None and field_name != '':
                error_subquery = error_subquery.filter(field_name=field_name)

            error_count = Subquery(error_subquery.values('asic_id').annotate(cnt=Count('id')).values('cnt')[:1],
                                   output_field=IntegerField())

            qs = qs.annotate(error_filter_count=Coalesce(error_count, 0)).filter(error_filter_count__gt=0)

        qs = qs.filter(stop_update=with_disabled_autoupdate)

        qs = qs.with_errors_and_warnings_count()

        if with_errors:
            qs = qs.filter(error_count__gt=0)

        if with_warnings:
            qs = qs.filter(warning_count__gt=0)

        if with_connection_errors:
            qs = qs.filter(connect_problems__gt=0)

        errors = errors.filter(asic_id__in=qs.values('id'))
        qs = qs.prefetch_related(
            Prefetch('errors', queryset=errors),
            Prefetch('chain_info_set', to_attr='chains'),
            Prefetch('fan_info_set', to_attr='fans'),
            'errors__error_rule'
        )
        qs = qs.with_farm_name().with_client_name()
        if unregistered_asics:
            qs = qs.filter(Q(farm_name=None) | Q(client_name=None))

        return qs.order_by('-error_count', '-warning_count').all()

    @login_required
    def resolve_asic_errors(self, info, asic_id, field_name, **kwargs):
        object_id = kwargs.get('object_id')
        queryset = models.Error.objects.filter(~Q(status=models.ErrorStatus.CLOSED), asic_id=asic_id,
                                               field_name=field_name).select_related('error_rule')
        if object_id is not None:
            return queryset.filter(object_id=object_id).order_by('-created')
        return queryset.order_by('-created')

    @login_required
    def resolve_dashboard_asics(self, info, **kwargs):
        errors = models.Error.objects.filter(~Q(status=models.ErrorStatus.CLOSED)) \
            .order_by('asic_id', 'field_name', 'level', 'object_id', '-created') \
            .distinct('asic_id', 'field_name', 'level', 'object_id')
        qs = models.Asic.objects.prefetch_related(
            Prefetch('errors', queryset=errors),
            Prefetch('chain_info_set', to_attr='chains'),
            Prefetch('fan_info_set', to_attr='fans'),
            'errors__error_rule'
        )
        qs = qs.with_errors_and_warnings_count().filter(Q(error_count__gt=0) & Q(connect_problems=0)) \
            .order_by('-error_count', '-warning_count')

        return qs

    @login_required
    def resolve_asic_settings(self, info, asic_id, **kwargs):
        try:
            asic = models.Asic.objects.get(pk=asic_id)
            return AsicSettings(username=asic.username, password=asic.password)
        except:
            return None


class CloseAsicErrors(graphene.Mutation, fields.AsicMutation):
    @login_required
    def mutate(self, info, asic_id):
        models.Error.objects.filter(asic_id=asic_id).update(status=models.ErrorStatus.CLOSED)
        return CloseAsicErrors(ok=True)


class StopUpdateAsic(graphene.Mutation, fields.AsicMutation):
    @login_required
    def mutate(self, info, asic_id):
        try:
            models.Asic.objects.filter(pk=asic_id).update(stop_update=True)
            return StopUpdateAsic(ok=True)
        except:
            return StopUpdateAsic(ok=False)


class ResumeUpdateAsic(graphene.Mutation, fields.AsicMutation):
    @login_required
    def mutate(self, info, asic_id):
        try:
            models.Asic.objects.filter(pk=asic_id).update(stop_update=False)
            return ResumeUpdateAsic(ok=True)
        except:
            return ResumeUpdateAsic(ok=False)


class UpdateAsic(graphene.Mutation, fields.AsicMutation):
    @login_required
    def mutate(self, info, asic_id):
        try:
            tasks.update_asic_info(asic_id)
            return UpdateAsic(ok=True)
        except:
            return UpdateAsic(ok=False)


class RebootAsic(graphene.Mutation, fields.AsicMutation):
    @login_required
    def mutate(self, info, asic_id):
        try:
            tasks.reboot_asic.delay(asic_id)
            return RebootAsic(ok=True)
        except:
            return RebootAsic(ok=False)


class GroupSetClient(graphene.Mutation, fields.OkField):
    class Arguments:
        asic_ids = graphene.List(graphene.Int)
        client_id = graphene.Int()

    @login_required
    def mutate(self, info, asic_ids, client_id):
        try:
            models.Asic.objects.filter(id__in=asic_ids).update(client_id=client_id)
            return GroupSetClient(ok=True)
        except:
            return GroupSetClient(ok=False)


class GroupSetFarm(graphene.Mutation, fields.OkField):
    class Arguments:
        asic_ids = graphene.List(graphene.Int)
        farm_id = graphene.Int()

    @login_required
    def mutate(self, info, asic_ids, farm_id):
        try:
            models.Asic.objects.filter(id__in=asic_ids).update(farm_id=farm_id)
            return GroupSetFarm(ok=True)
        except:
            return GroupSetFarm(ok=False)


class SetAutoupdateAll(graphene.Mutation, fields.OkField):
    class Arguments:
        asic_ids = graphene.List(graphene.Int)
        update = graphene.Boolean()

    @login_required
    def mutate(self, info, asic_ids, update):
        try:
            models.Asic.objects.filter(id__in=asic_ids).update(stop_update=not update)
            return SetAutoupdateAll(ok=True)
        except:
            return SetAutoupdateAll(ok=False)


class SetPassword(graphene.Mutation, fields.OkField):
    class Arguments:
        asic_id = graphene.Int()
        password = graphene.String()

    @login_required
    def mutate(self, info, asic_id, password):
        try:
            asic = models.Asic.objects.get(pk=asic_id)
            asic.change_password(password)
            return SetPassword(ok=True)
        except models.Asic.DoesNotExist:
            return SetPassword(ok=False)


class SetAsicType(graphene.Mutation, fields.AsicMutation):
    class Arguments:
        type = graphene.Int()
        asic_id = graphene.NonNull(graphene.Int)

    result = graphene.String()

    @login_required
    def mutate(self, info, asic_id, type):
        try:
            asic = models.Asic.objects.get(pk=asic_id)
            asic.type = type
            asic.name = asic.get_type_display()
            asic.save()

            return SetAsicType(ok=True, result=asic.get_type_display())
        except:
            return SetAsicType(ok=False)


class SetAlgType(graphene.Mutation, fields.AsicMutation):
    class Arguments:
        type = graphene.Int()
        asic_id = graphene.NonNull(graphene.Int)

    result = graphene.String()

    @login_required
    def mutate(self, info, asic_id, type):
        try:
            asic = models.Asic.objects.get(pk=asic_id)
            asic.alg_type = type
            asic.save()

            return SetAlgType(ok=True, result=asic.get_alg_type_display())
        except:
            return SetAlgType(ok=False)


class AddAsic(graphene.Mutation, fields.OkField):
    class Arguments:
        type = graphene.Int()
        ip_address = graphene.String()
        farm = graphene.Int()
        client = graphene.Int()
        alg_type = graphene.Int()

    @login_required
    def mutate(self, info, type, ip_address, alg_type, farm=None, client=None):
        asic = models.Asic(
            type=type,
            ip_address=ip_address,
            farm=farm,
            client=client,
            alg_type=alg_type,
        )
        asic.save()
        return AddAsic(ok=True)


class AsicMutations(object):
    close_asic_errors = CloseAsicErrors.Field()
    stop_update_asic = StopUpdateAsic.Field()
    resume_update_asic = ResumeUpdateAsic.Field()
    update_asic = UpdateAsic.Field()
    reboot_asic = RebootAsic.Field()
    group_set_client = GroupSetClient.Field()
    group_set_farm = GroupSetFarm.Field()
    set_autoupdate_all = SetAutoupdateAll.Field()
    asic_set_password = SetPassword.Field()
    set_asic_type = SetAsicType.Field()
    set_alg_type = SetAlgType.Field()
    add_asic = AddAsic.Field()
