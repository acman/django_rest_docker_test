import datetime

from django.conf import settings
from django.db import models
from django.db.models import Sum, F, DecimalField
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    SHIPMENT_PERIOD = 5
    NEW, IN_PROGRESS, SHIPPED, COMPLETED, CANCELLED = range(1, 6)
    STATUS_CHOICES = (
        (NEW, _('new')),
        (IN_PROGRESS, _('in progress')),
        (SHIPPED, _('shipped')),
        (COMPLETED, _('completed')),
        (CANCELLED, _('cancelled')),
    )

    status = models.PositiveIntegerField(_('status'), choices=STATUS_CHOICES, default=NEW, db_index=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='orders',
                               on_delete=models.SET_NULL)
    products = models.ManyToManyField('products.Product', verbose_name=_('products'), through='OrderProductMembership')
    shipping_details = models.TextField(_('shipping details'), blank=True)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True, db_index=True)
    shipment_date = models.DateTimeField(_('shipment date'), blank=True, null=True)
    close_date = models.DateTimeField(_('close date'), blank=True, null=True, db_index=True)
    total_price = models.DecimalField(
        _(u'sum of all the products prices'), max_digits=10, decimal_places=2, blank=True, null=True, default=None,
        help_text=_(u'Sum of all the products prices and their quantities.')
    )

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ('created_date', )

    def __str__(self):
        return f'{self.client} order #{self.pk}, status {self.status}'

    def _set_shipment_date(self):
        if self.pk is None:
            self.shipment_date = datetime.datetime.utcnow() + datetime.timedelta(days=self.SHIPMENT_PERIOD)

    def _calculate_total_price(self):
        self.total_price = self.orderproductmembership_set.aggregate(
            total=Sum(F('product__price') * F('quantity'), output_field=DecimalField()))['total']

    def _close_order(self):
        if self.status == self.COMPLETED:
            self.close_date = datetime.datetime.utcnow()

    def save(self, **kwargs):
        self._set_shipment_date()
        self._calculate_total_price()
        self._close_order()
        super().save()


class OrderProductMembership(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
