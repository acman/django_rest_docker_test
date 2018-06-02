from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_('name'), max_length=100)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{name} - {price}'