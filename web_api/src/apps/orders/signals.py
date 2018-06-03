from django.db.models import Sum, F, DecimalField
from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Order


@receiver(post_save, sender=Order)
def update_total_price(sender, instance, created, **kwargs):
    post_save.disconnect(update_total_price, sender=Order)
    instance.total_price = instance.orderproductmembership_set.aggregate(
        total=Sum(F('product__price') * F('quantity'), output_field=DecimalField()))['total']
    instance.save()
    post_save.connect(update_total_price, sender=Order)
