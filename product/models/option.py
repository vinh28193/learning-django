from django.db import models
from django.utils.translation import gettext_lazy as _
from store.models import Store
from user.models import User
from .product import Product
from .variant import ProductVariant


class ProductOption(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_options"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="product_options"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="options"
    )
    name = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_option'
        db_tablespace = 'product'
        verbose_name = _("product option")
        verbose_name_plural = _("product options")


class ProductOptionValue(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_option_values"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="product_option_values"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="option_values"
    )
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="values"
    )
    option = models.ForeignKey(
        ProductOption, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'product_option_value'
        db_tablespace = 'product'
        verbose_name = _("product option value")
        verbose_name_plural = _("product option values")
