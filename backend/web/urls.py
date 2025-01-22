# -*- coding: utf-8 -*-
from django.conf.urls import url

from backend.web.views import HomeView, UpdateAsic, DashboardView, GroupEdit, ErrorView, WarningView, PendingError, CloseError, \
    ToWarning, ToError, CloseAllErrors, StopUpdateAsic, ResumeUpdateAsic

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),
    url(r'^update_asic/(?P<pk>\d+)$', UpdateAsic.as_view(), name='update_asic'),
    url(r'^group_edit$', GroupEdit.as_view(), name='group_edit'),
    url(r'^errors$', ErrorView.as_view(), name='errors'),
    url(r'^warnings$', WarningView.as_view(), name='warnings'),
    url(r'^to_pending/(?P<pk>\d+)$', PendingError.as_view(), name='to_pending'),
    url(r'^close_error/(?P<pk>\d+)$', CloseError.as_view(), name='close_error'),
    url(r'^close_all_errors/(?P<pk>\d+)$', CloseAllErrors.as_view(), name='close_all_errors'),
    url(r'^stop_update_asic/(?P<pk>\d+)$', StopUpdateAsic.as_view(), name='stop_update_asic'),
    url(r'^resume_update_asic/(?P<pk>\d+)$', ResumeUpdateAsic.as_view(), name='resume_update_asic'),
    url(r'^to_warning/(?P<pk>\d+)$', ToWarning.as_view(), name='to_warning'),
    url(r'^to_error/(?P<pk>\d+)$', ToError.as_view(), name='to_error'),
]
