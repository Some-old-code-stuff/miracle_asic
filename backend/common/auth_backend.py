# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User

import backend.common.models as models
from backend.common.functions import check_token


class SmsTokenBackend:
    def authenticate(self, request, username=None, password=None):
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                u = User(username=settings.ADMIN_USERNAME, password=settings.ADMIN_PASSWORD, is_staff=True, is_superuser=True)
                u.save()
                return u

        token_valid, try_count = check_token(username, password)
        if token_valid:
            return models.UserProfile.objects.get(phone=username).user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Djano Admin treats None user as anonymous your who have no right at all.
            return None
