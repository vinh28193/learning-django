from calendar import timegm
from collections import OrderedDict
from datetime import timedelta, datetime

import jwt
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework_jwt.compat import get_username_field
from rest_framework_jwt.settings import api_settings

from user.utils.jwt import get_store_field

username_validator = UnicodeUsernameValidator()

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class Serializer(serializers.Serializer):

    def get_auth(self):
        return self.validated_data["user"], self.validated_data["store"], self.validated_data["token"]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class JSONWebTokenSerializer(Serializer):
    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(
            validators=[username_validator], required=True
        )
        self.fields['password'] = serializers.CharField(required=True)
        self.fields[get_store_field()] = serializers.CharField(required=False)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):

        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        user = authenticate(**credentials)

        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg)
            store = None
            if attrs.get(get_store_field()):
                from store.models import Store
                try:
                    store = Store.objects.get(pk=attrs[get_store_field()])
                except Store.DoesNotExist:
                    msg = _('Unable to access to not available store.')
                    raise serializers.ValidationError(msg)

            payload = jwt_payload_handler(user, store=store)

            return OrderedDict(
                user=user, store=store, token=jwt_encode_handler(payload)
            )
        else:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg)


class VerificationBaseSerializer(Serializer):
    """
    Abstract serializer used for verifying and refreshing JWTs.
    """
    token = serializers.CharField()

    def validate(self, attrs):
        msg = 'Please define a validate method.'
        raise NotImplementedError(msg)

    # noinspection PyMethodMayBeStatic
    def check_payload(self, token):
        # Check payload valid (based off of JSONWebTokenAuthentication,
        # may want to refactor)
        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = _('Signature has expired.')
            raise serializers.ValidationError(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise serializers.ValidationError(msg)

        return payload

    # noinspection PyMethodMayBeStatic
    def check_user(self, payload):
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise serializers.ValidationError(msg)

        # Make sure user exists
        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = _("User doesn't exist.")
            raise serializers.ValidationError(msg)

        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)

        return user


class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Check the veracity of an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self.check_payload(token=token)
        user = self.check_user(payload=payload)

        return OrderedDict(user=user, token=token)


class RefreshJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Refresh an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self.check_payload(token=token)
        user = self.check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, timedelta):
                refresh_limit = (
                    (refresh_limit.days * 24 * 3600) + refresh_limit.seconds
                )

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat

        return OrderedDict(token=jwt_encode_handler(new_payload), user=user)
