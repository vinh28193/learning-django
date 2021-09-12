from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser, models.Model):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        blank=True,
        null=True,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ '
            'only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    phone = models.CharField(
        _("phone number"),
        max_length=20,
        unique=True,
        error_messages={
            'unique': _("A user with that phone number already exists."),
        },

    )

    email = models.EmailField(
        _('email address'),
        blank=True,
        null=True,
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },

    )

    avatar_image = models.CharField(
        _("avatar image"), max_length=255, blank=True, null=True
    )

    language = models.CharField(
        _("language"), max_length=5, default=settings.LANGUAGE_CODE
    )
    timezone = models.CharField(
        _("timezone"), max_length=20, default=settings.TIME_ZONE
    )

    class Meta:
        db_table = "user"
        db_tablespace = "user"
        verbose_name = _("User")
