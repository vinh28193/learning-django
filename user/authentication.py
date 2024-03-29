import jwt
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from .utils import (
    jwt_get_user_pk_from_payload_handler,
    jwt_get_store_pk_from_payload_handler
)

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class StoreAccessMixin:

    def get_store_model(self):
        from store.models import Store
        return Store

    def access_credentials(self, payload):
        pk = jwt_get_store_pk_from_payload_handler(payload)

        if not pk:
            return None
        StoreModel = self.get_store_model()
        try:
            store = StoreModel.objects.get(pk=pk)
        except StoreModel.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        # if not store.is_active:
        #     msg = _('Store accessing is disabled.')
        #     raise exceptions.AuthenticationFailed(msg)
        return store

    def grant_request(self, request, store):
        request.store = store
        request._request.store = store
        return request


class JWTAuthentication(StoreAccessMixin, JSONWebTokenAuthentication):

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)
        store = self.access_credentials(payload)
        if store:
            self.grant_request(request, store)
        return user, payload

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        pk = jwt_get_user_pk_from_payload_handler(payload)

        if not pk:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise exceptions.AuthenticationFailed(msg)

        return user
