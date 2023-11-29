from django.db import models
from user.models import User


class Store(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stores"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    domain = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    timezone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "store"
        db_tablespace = "store"
        verbose_name = "store"
        verbose_name_plural = "stores"
