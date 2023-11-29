from django.utils.translation import gettext_lazy as _
from django.db import models

from store.models import Store
from user.models import User
from .product import Product


class Image(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_images"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="product_images"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    position = models.PositiveIntegerField()
    src = models.URLField()
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = "product_image"
        db_tablespace = "product"
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
