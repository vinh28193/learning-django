from django.utils.translation import gettext_lazy as _
from django.db import models

from store.models import Store
from user.models import User


class VendorQuerySet(models.QuerySet):
    """'Vendor QuerySet"""


class VendorManager(models.Manager.from_queryset(VendorQuerySet)):
    """'Vendor Manager"""


class ProductVendor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_vendors"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="product_vendors"
    )
    name = models.CharField(_('vendor name'), max_length=255)

    logo = models.CharField(_('logo'), max_length=255, null=True, blank=True)

    active = models.BooleanField(_('active'), default=True)

    created_at = models.DateTimeField(
        _('created at'), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'), auto_now=True
    )

    class Meta:
        db_table = "product_vendor"
        db_tablespace = "product"
        verbose_name = _("product vendor")
        verbose_name_plural = _("product vendors")
