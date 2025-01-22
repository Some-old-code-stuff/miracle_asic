# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from backend.common.models import Asic, AsicInfo, Client, Farm, ErrorRule


class AsicInfoSearchForm(ModelForm):
    class Meta:
        model = AsicInfo
        fields = ['asic_name', 'pool_status' ]


class AsicSearchForm(ModelForm):
    def __init__(self, *args,**kwargs):
        super(AsicSearchForm, self).__init__(*args,**kwargs)
        self.fields['farm'].required = False
        self.fields['client'].required = False
        self.fields['type'].required = False
        self.fields['alg_type'].required = False
        self.fields['ip_address'].required = False
        self.fields['type'].choices = [('','---------')] + self.fields['type'].choices
        self.fields['alg_type'].choices = [('','---------')] + self.fields['alg_type'].choices

    class Meta:
        model = Asic
        fields = ["type", 'alg_type', 'farm', 'client', 'asic_name', 'ip_address', 'pool_status', ]


class ClientSearchForm(ModelForm):
    prefix = 'client'

    def __init__(self, *args,**kwargs):
        super(ClientSearchForm, self).__init__(*args,**kwargs)
        self.fields['name'].required = False

    class Meta:
        model = Client
        fields = ['name']


class FarmSearchForm(ModelForm):

    prefix = 'farm'

    def __init__(self, *args,**kwargs):
        super(FarmSearchForm, self).__init__(*args,**kwargs)
        self.fields['name'].required = False

    class Meta:
        model = Farm
        fields = ['name']


class ErrorRuleSearchForm(ModelForm):
    prefix = 'error_rule'

    def __init__(self, *args,**kwargs):
        super(ErrorRuleSearchForm, self).__init__(*args,**kwargs)
        self.fields['error_level'].required = False
        self.fields['field_name'].required = False
        self.fields['error_level'].choices = [('','---------')] + self.fields['error_level'].choices
        self.fields['field_name'].choices = [('','---------')] + self.fields['field_name'].choices

    class Meta:
        model = ErrorRule
        fields = ['error_level', 'field_name']


class AsicGroupEditForm(ModelForm):
    asic_ids = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model=Asic
        fields = ['client', 'farm']

    def __init__(self, *args, **kwargs):
        super(AsicGroupEditForm, self).__init__(*args, **kwargs)
        self.fields['client'].required = False
        self.fields['farm'].required = False