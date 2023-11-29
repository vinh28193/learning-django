from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User
from store.models import Store
from .product import Product
from .image import Image


class ProductVariant(models.Model):

    class InventoryPolicy(models.TextChoices):
        DENY = 1, _('Deny')
        CONTINUE = 2, _("Continue")

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_variants"
    )
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="product_variants"
    )

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )

    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="variants"
    )
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    compare_at_price = models.DecimalField(
        max_digits=13, decimal_places=2, default=0
    )
    price = models.DecimalField(
        max_digits=13, decimal_places=2, default=0
    )
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = models.CharField(max_length=10)
    taxable = models.BooleanField()
    tax_code = models.CharField(max_length=255)
    fulfillment_service = models.CharField(max_length=255)

    inventory_item_id = models.IntegerField()
    inventory_management = models.CharField(max_length=100, default="default")
    inventory_policy = models.CharField(max_length=100, default="deny")
    inventory_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'product_variant'
        db_tablespace = 'product'
        verbose_name = _("product variant")
        verbose_name_plural = _("product variants")
