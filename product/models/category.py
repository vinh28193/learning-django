from django.utils.translation import gettext_lazy as _
from django.db import models


class CategoryQuerySet(models.QuerySet):
    """Category QuerySet"""


class CategoryManager(models.Manager.from_queryset(CategoryQuerySet)):
    """Category Manager"""


class Category(models.Model):

    name = models.CharField(_('category name'), max_length=255)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        _('created at'), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('updated at'), auto_now=True
    )

    class Meta:
        db_table = "category"
        db_tablespace = "product"
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")
