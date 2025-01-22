# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import JsonResponse
from graphene_django.views import GraphQLView
from graphql import GraphQLCoreBackend
from silk.profiling.profiler import silk_profile

from backend.common.tasks import update_asic_info
from django.contrib import messages
from django.db import models
from django.db.models import OuterRef
from django.db.models import Subquery, Count
from django.db.models.functions import Coalesce
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from backend.common.models import Asic, Error, ErrorLevel, ErrorStatus
from backend.web.forms import AsicSearchForm, ClientSearchForm, FarmSearchForm, AsicGroupEditForm, \
    ErrorRuleSearchForm


class FilterListView(ListView):
    equal_fields = []
    string_fields = []
    gte_fields = []
    lte_fields = []
    filter_forms = []
    default_sort = []

    @staticmethod
    def convert_field_name(string):
        return string.replace('-', '__')

    def get_queryset(self):
        context = self.queryset

        for field_name in self.equal_fields:
            if field_name in self.request.GET:
                field_value = self.request.GET.get(field_name)
                if field_value != '':
                    context = context.filter(**{FilterListView.convert_field_name(field_name): field_value})

        for field_name in self.string_fields:
            if field_name in self.request.GET and self.request.GET.get(field_name) != '':
                context = context.filter(**{
                    '{}__icontains'.format(FilterListView.convert_field_name(field_name)): self.request.GET.get(
                        field_name)})

        for field_name in self.gte_fields:
            if field_name in self.request.GET:
                context = context.filter(**{
                    '{}__gte'.format(FilterListView.convert_field_name(field_name)): self.request.GET.get(field_name)})

        for field_name in self.lte_fields:
            if field_name in self.request.GET:
                context = context.filter(**{
                    '{}__lte'.format(FilterListView.convert_field_name(field_name)): self.request.GET.get(field_name)})

        sort_by = self.request.GET.get('sort_by', 'id')

        self.default_sort.append(sort_by)

        return context.order_by(*self.default_sort)

    def get_context_data(self, **kwargs):
        context = super(FilterListView, self).get_context_data(**kwargs)
        context['filter_forms'] = list(map(lambda x: x(self.request.GET), self.filter_forms))
        context['current_sort_field'] = self.request.GET.get('sort_by', '')
        context['all_count'] = self.get_queryset().count()
        return context


class HomeView(FilterListView):
    template_name = 'home.html'
    model = Asic
    context_object_name = 'asics'
    paginate_by = 20
    queryset = Asic.objects.all().with_errors_and_warnings_count()

    default_sort = ['-error_count', '-warning_count']
    title = 'Home'
    filter_forms = [
        AsicSearchForm,
        ClientSearchForm,
        FarmSearchForm,
        ErrorRuleSearchForm,
    ]

    equal_fields = [
        'type',
        'alg_type',
        'farm',
        'client',
    ]

    string_fields = [
        'client-name',
        'farm-name',
        'ip_address',
        'asic_name',
        'pool_status',
    ]

    error_rule_fields = [
        'error_rule-error_level',
        'error_rule-field_name',
    ]

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['group_form'] = AsicGroupEditForm()

        return context

    def get_queryset(self):

        error_level = self.request.GET.get('error_rule-error_level', None)
        field_name = self.request.GET.get('error_rule-field_name', None)
        if error_level is None and field_name is None:
            return super(HomeView, self).get_queryset()

        context = self.queryset

        # Надо найти все асики с ошибками с таким полем

        error_subquery = Error.objects.filter(asic=OuterRef('id'))

        if error_level is not None and error_level != '':
            error_subquery = error_subquery.filter(level=error_level)
        if field_name is not None and field_name != '':
            error_subquery = error_subquery.filter(error_rule__field_name=field_name)

        error_count = Subquery(error_subquery.values('asic_id').annotate(cnt=Count('id')).values('cnt')[:1],
                               output_field=models.IntegerField())

        context = context.annotate(error_filter_count=Coalesce(error_count, 0)).filter(error_filter_count__gt=0)

        self.queryset = context

        return super(HomeView, self).get_queryset()


class UpdateAsic(View):
    def get(self, request, pk):
        try:
            update_asic_info.delay(pk)
            messages.success(request, u'ASIC успешно поставлен в очередь на обновление!')
        except Exception as e:
            messages.error(request, u'К сожалению, произошла ошибка при постановке ASIC в очредь на обновление. '
                                    u'Обратитесь к системному администратору.')

        return redirect('home', permanent=False)


class GroupEdit(View):
    def post(self, request):
        form = AsicGroupEditForm(request.POST)
        if not form.is_valid():
            messages.error(request, u'Выделите ASIC для применения операции')
            return redirect('home', permanent=False)
        asic_ids = form.cleaned_data['asic_ids'].split(',')
        if form.cleaned_data['client'] is not None:
            Asic.objects.filter(pk__in=asic_ids).update(client=form.cleaned_data['client'])
        if form.cleaned_data['farm'] is not None:
            Asic.objects.filter(pk__in=asic_ids).update(farm=form.cleaned_data['farm'])

        messages.success(request, u'Групповая операция успешно произведена')

        return redirect('home', permanent=False)


class DashboardView(ListView):
    template_name = 'dashboard.html'
    model = Asic
    context_object_name = 'asics'
    queryset = Asic.objects.all().with_errors_and_warnings_count().order_by('-error_count', '-warning_count')
    # queryset = Asic.objects.filter(ip_address='192.168.8.100').annotate(error_count=Count('errors'))


class ErrorView(ListView):
    template_name = 'errors.html'
    model = Error
    context_object_name = 'errors'
    queryset = Error.get_current_errors()
    paginate_by = 20


class PendingError(View):
    def get(self, request, pk):
        try:
            error = Error.objects.get(pk=pk)
            error.status = ErrorStatus.PENDING
            error.save()
            messages.success(request, 'Ошибка успешно отправлена в разработку!')
        except Error.DoesNotExist:
            messages.error(request, 'Невозможно отправить ошибку в разработку!')
        return redirect('errors', permanent=False)


class CloseError(View):
    def get(self, request, pk):
        try:
            error = Error.objects.get(pk=pk)
            error.status = ErrorStatus.CLOSED
            error.save()
            messages.success(request, 'Ошибка успешно решена!')
        except Error.DoesNotExist:
            messages.error(request, 'Невозможно поставить статус "Решена" этой ошибке!')
        return redirect('errors', permanent=False)


class ToWarning(View):
    def get(self, request, pk):
        try:
            error = Error.objects.get(pk=pk)
            error.level = ErrorLevel.WARN
            error.save()
            messages.success(request, 'Уровень ошибки успешно понижен до уведомления!')
        except Error.DoesNotExist:
            messages.error(request, 'Невозможно понизить уровень этой ошибки!')
        return redirect('errors', permanent=False)


class ToError(View):
    def get(self, request, pk):
        try:
            error = Error.objects.get(pk=pk)
            error.level = ErrorLevel.ERROR
            error.save()
            messages.success(request, 'Уровень уведомления успешно повышен до ошибки!')
        except Error.DoesNotExist:
            messages.error(request, 'Невозможно повысить уровень этого уведомления!')
        return redirect('errors', permanent=False)


class WarningView(ListView):
    template_name = 'errors.html'
    model = Error
    context_object_name = 'errors'
    queryset = Error.get_current_warnings().order_by('-created')
    paginate_by = 100


class CloseAllErrors(View):
    def get(self, request, pk):
        try:
            asic = Asic.objects.get(pk=pk)
            asic.errors.update(status=ErrorStatus.CLOSED)
            messages.success(request, 'Все ошибки по ASIC закрыты!')
        except Asic.DoesNotExist:
            messages.error(request, 'ASIC не найден!')
        return redirect('home', permanent=False)


class StopUpdateAsic(View):
    def get(self, request, pk):
        try:
            asic = Asic.objects.get(pk=pk)
            asic.stop_update = True
            asic.save()
            messages.success(request, 'Автообновление ASIC успешно отключено!')
        except Asic.DoesNotExist:
            messages.error(request, 'ASIC не найден!')
        return redirect('home', permanent=False)


class ResumeUpdateAsic(View):
    def get(self, request, pk):
        try:
            asic = Asic.objects.get(pk=pk)
            asic.stop_update = False
            asic.save()
            messages.success(request, 'Автообновление ASIC успешно включено!')
        except Asic.DoesNotExist:
            messages.error(request, 'ASIC не найден!')
        return redirect('home', permanent=False)


class GraphqlApiView(View):
    # @silk_profile()
    def post(self, request):
        from main.schema import main_schema
        json_request = json.loads(request.body)
        document = GraphQLCoreBackend().document_from_string(main_schema, json_request['query'])
        variables = json_request.get('variables', None)
        if variables is not None:
            data = document.execute(variables=variables, context=request)
        else:
            data = document.execute(context=request)
        from django.http import HttpResponse
        errors = []
        if data.errors is not None:
            errors = [GraphQLView.format_error(e) for e in data.errors]

        result = {'data': data.data, 'errors': errors}
        from django.core.serializers.json import DjangoJSONEncoder
        return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder))
