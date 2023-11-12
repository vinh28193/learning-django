from django.db import models
from django.utils.translation import gettext_lazy as _
from .product import Product
from .variant import Variant


class Option(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    position = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_option'
        db_tablespace = 'product'
        verbose_name = _("product option")
        verbose_name_plural = _("product options")


class OptionValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = 'product_option_value'
        db_tablespace = 'product'
        verbose_name = _("product option value")
        verbose_name_plural = _("product option values")
