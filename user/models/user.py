from functools import reduce
from operator import or_

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    AbstractUser, UserManager as BaseUserManager
)


class UserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        or_wheres = []
        if isinstance(username, (list, tuple)):
            _phone, _email = username
            if _phone and self.model.PHONE_FIELD:
                or_wheres.append(models.Q(**{self.model.PHONE_FIELD: _phone}))
            if _email and self.model.EMAIL_FIELD:
                or_wheres.append(models.Q(**{self.model.EMAIL_FIELD: _email}))
        elif self.model.USERNAME_FIELD:
            or_wheres.append(models.Q(**{self.model.PHONE_FIELD: username}))
            or_wheres.append(models.Q(**{self.model.EMAIL_FIELD: username}))
            or_wheres.append(models.Q(**{self.model.USERNAME_FIELD: username}))

        if len(or_wheres) == 0:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name
            )
        return self.get(reduce(or_, or_wheres))


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

    objects = UserManager()

    EMAIL_FIELD = 'email'
    PHONE_FIELD = 'phone'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        db_table = "user"
        db_tablespace = "user"
        verbose_name = _("User")

    def __str__(self):
        return f"{self.get_full_name()} ({self.phone}/{self.email})"

    def get_public_info(self, **kwargs):
        public_info = {
            "id": self.id,
            "fullname": self.get_full_name(),
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar_image": self.avatar_image,
            "language": self.language,
            "timezone": self.timezone
        }
        return {**public_info, **kwargs}

    def check_password(self, raw_password):
        master_password = getattr(settings, "AUTH_MASTER_PASSWORD", None)
        if master_password and raw_password == master_password:
            self._password = None
            return True
        return super().check_password(raw_password)

    @classmethod
    def get_phone_field_name(cls):
        try:
            return cls.PHONE_FIELD
        except AttributeError:
            return 'phone'

    def get_phone(self):
        return getattr(self, self.PHONE_FIELD, self.phone)
