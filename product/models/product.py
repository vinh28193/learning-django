from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from store.models import Store
from .category import ProductCategory
from .vendor import ProductVendor


class Product(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        ARCHIVED = 'archived', _("Archived")
        DRAFT = 'draft', _('Draft')

    class PublishedScope(models.TextChoices):
        GLOBAL = 'global', _("Global")
        STORE_FRONT = 'store_front', _("Store Front")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="products"
    )
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
        ProductCategory,
        verbose_name=_('product category'),
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
    )
    vendor = models.ForeignKey(
        ProductVendor,
        verbose_name=_('product vendor'),
        related_name="products",
        null=True,
        on_delete=models.SET_NULL
    )
    status = models.CharField(
        _("status"), max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )
    created_by = models.IntegerField(default=None, null=True)

    created_at = models.DateTimeField(
        _('created at'), auto_now_add=True
    )
    updated_by = models.IntegerField(default=None, null=True)
    updated_at = models.DateTimeField(
        _('updated at'), auto_now=True
    )
    published_by = models.IntegerField(default=None, null=True)
    published_at = models.DateTimeField(_('published at'))

    class Meta:
        db_table = 'product'
        db_tablespace = 'product'
        verbose_name = _("product")
        verbose_name_plural = _("products")
