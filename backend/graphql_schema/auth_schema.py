# -*- coding: utf-8 -*-
import hashlib

import graphene
from django.conf import settings
from django.utils import timezone

import backend.common.models as models
from backend.common.functions import send_token, check_token


class SendTokenMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String()
        pass
    ok = graphene.Boolean()
    token = graphene.String()

    def mutate(self, info, phone):
        token = send_token(phone)
        if settings.DEBUG:
            return SendTokenMutation(ok=True, token=token)
        return SendTokenMutation(ok=True)


class CheckTokenMutation(graphene.Mutation):
    class Arguments:
        phone = graphene.String()
        token = graphene.String()
        pass
    ok = graphene.Boolean()
    try_count = graphene.Int()

    def mutate(self, info, phone, token):
        ok, try_count = check_token(phone, token)
        return CheckTokenMutation(ok=ok, try_count=try_count)


class AuthMutations(object):
    send_sms_token = SendTokenMutation.Field()
    check_sms_token = CheckTokenMutation.Field()
