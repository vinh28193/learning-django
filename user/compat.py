from django.contrib.auth import get_user_model

try:
    import simplejson as json
except ImportError:
    import json

User = get_user_model()


def get_username_field():
    try:
        username_field = User.USERNAME_FIELD
    except AttributeError:
        username_field = 'username'

    return username_field


def get_username(user):
    try:
        username = user.get_username()
    except AttributeError:
        username = user.username

    return username


def get_email_field():
    try:
        email_field = User.get_email_field_name()
    except AttributeError:
        email_field = 'email'
    return email_field


def get_email(user):
    try:
        email = user.get_email()
    except AttributeError:
        email = user.email

    return email


def get_phone_field():
    try:
        phone_field = User.get_phone_field_name()
    except AttributeError:
        phone_field = 'phone'

    return phone_field


def get_phone(user):
    try:
        phone = user.get_phone()
    except AttributeError:
        phone = user.phone

    return phone
