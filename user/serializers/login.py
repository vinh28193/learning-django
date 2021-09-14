from collections import OrderedDict
from rest_framework import serializers
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, validators=[username_validator]
    )
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                return OrderedDict(user=user)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

    def get_user(self):
        return self.validated_data["user"]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
