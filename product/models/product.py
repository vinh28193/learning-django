from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from .category import Category
from .vendor import Vendor


class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        ARCHIVED = 'archived', _("Archived")
        DRAFT = 'draft', _('Draft')

    class PublishedScope(models.TextChoices):
        GLOBAL = 'global', _("Global")
        STORE_FRONT = 'store_front', _("Store Front")

    title = models.CharField(
        _('product name'),
        max_length=255,
        null=False,
        blank=False
    )
    handle = models.CharField(
        _('handle'),
        max_length=50,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('product category'),
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
    )
    vendor = models.ForeignKey(
        Vendor,
        verbose_name=_('product vendor'),
        related_name="products",
        null=True,
        on_delete=models.SET_NULL
    )

    created_by = models.ForeignKey(
        User,
        verbose_name=_('created by'),
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        _('created at'), auto_now_add=True
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name=_('updated by'),
        on_delete=models.CASCADE
    )
    updated_at = models.DateTimeField(
        _('updated at'), auto_now=True
    )
    published_by = models.ForeignKey(
        User,
        verbose_name=_('published by'),
        on_delete=models.CASCADE
    )
    published_at = models.DateTimeField(_('published at'))
    published_scope = models.CharField(
        _('published scope'),
        max_length=20,
        choices=PublishedScope.choices,
        default=PublishedScope.GLOBAL
    )
    status = models.CharField(
        _("status"), max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    class Meta:
        db_table = 'product'
        db_tablespace = 'product'
        verbose_name = _("product")
        verbose_name_plural = _("products")
