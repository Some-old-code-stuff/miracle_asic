# -*- coding: utf-8 -*-
from django.urls import re_path

from backend.web.views import HomeView, UpdateAsic, DashboardView, GroupEdit, ErrorView, WarningView, PendingError, CloseError, \
    ToWarning, ToError, CloseAllErrors, StopUpdateAsic, ResumeUpdateAsic

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^dashboard$', DashboardView.as_view(), name='dashboard'),
    re_path(r'^update_asic/(?P<pk>\d+)$', UpdateAsic.as_view(), name='update_asic'),
    re_path(r'^group_edit$', GroupEdit.as_view(), name='group_edit'),
    re_path(r'^errors$', ErrorView.as_view(), name='errors'),
    re_path(r'^warnings$', WarningView.as_view(), name='warnings'),
    re_path(r'^to_pending/(?P<pk>\d+)$', PendingError.as_view(), name='to_pending'),
    re_path(r'^close_error/(?P<pk>\d+)$', CloseError.as_view(), name='close_error'),
    re_path(r'^close_all_errors/(?P<pk>\d+)$', CloseAllErrors.as_view(), name='close_all_errors'),
    re_path(r'^stop_update_asic/(?P<pk>\d+)$', StopUpdateAsic.as_view(), name='stop_update_asic'),
    re_path(r'^resume_update_asic/(?P<pk>\d+)$', ResumeUpdateAsic.as_view(), name='resume_update_asic'),
    re_path(r'^to_warning/(?P<pk>\d+)$', ToWarning.as_view(), name='to_warning'),
    re_path(r'^to_error/(?P<pk>\d+)$', ToError.as_view(), name='to_error'),
]
