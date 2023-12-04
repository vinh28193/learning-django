from calendar import timegm
from datetime import datetime

from rest_framework_jwt.settings import api_settings

from user.compat import (
    get_username_field, get_username, get_phone_field,
    get_phone, get_email_field, get_email
)


def get_store_field():
    return "store_id"


def get_store_id(store):
    return store and store.pk or None


def jwt_payload_handler(user, store=None):
    payload = {'id': user.pk}
    payload.update({
        get_username_field(): get_username(user),
        get_phone_field(): get_phone(user),
        get_email_field(): get_email(user),
    })
    payload[get_store_field()] = get_store_id(store)
    payload['exp'] = datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    return payload


def jwt_get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    if payload.get(get_username_field()):
        return payload[get_username_field()]
    return payload.get(get_username_field()), payload.get(get_email_field())


def jwt_response_payload_handler(token, user=None, store=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """

    if isinstance(user, object) and hasattr(user, "get_public_info"):
        user = user.get_public_info()

    return {'token': token, 'user': user, "store": {}}


def jwt_get_user_pk_from_payload_handler(payload):
    """
    Override this function if user_id is formatted differently in payload
    """
    return payload["id"]


def jwt_get_store_pk_from_payload_handler(payload):
    return payload.get(get_store_field())
