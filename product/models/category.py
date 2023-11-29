from django.utils.translation import gettext_lazy as _
from django.db import models
from store.models import Store
from user.compat import User


class CategoryQuerySet(models.QuerySet):
    """Category QuerySet"""


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    """Category Manager"""


class ProductCategory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_categories"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="product_categories"
    )
    name = models.CharField(_('category name'), max_length=255)

    created_at = models.DateTimeField(
        _('created at'), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'), auto_now=True
    )

    class Meta:
        db_table = "product_category"
        db_tablespace = "product"
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")
