from rest_framework import viewsets

from .models import Order
from .permissions import AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly
from .serializers import OrderListSerializer, OrderCreateUpdatePatchSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Return an order instance.

        list:
            Return all orders.
            Can be filtered by created_date__range:
                /orders/?created_date__range=[2018-06-03,2018-06-04]

        create:
            Create a new order.
            Request example:
                {"shipping_details": "shipping details", "products": [{"id": 1,"quantity": 3},{"id": 2,"quantity": 5}]}

        delete:
            Remove an existing order.

        partial_update:
            Update one or more fields on an existing order.

        update:
            Update an order.
    """

    serializers = {
        'default': OrderListSerializer,
        'create': OrderCreateUpdatePatchSerializer,
        'update': OrderCreateUpdatePatchSerializer,
        'patch': OrderCreateUpdatePatchSerializer,
    }
    permission_classes = (AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly, )

    def _get_filters(self):
        filters = {}
        created_date_range = self.request.GET.get('created_date__range')
        if created_date_range:
            date_min, date_max = created_date_range.split(',')
            filters['created_date__range'] = [date_min[1:], date_max[:-1]]

        return filters

    def get_queryset(self):
        return Order.objects.filter(**self._get_filters())

    def get_serializer_class(self):
        """
        Return default if serializer for action not created.
        """
        return self.serializers[self.action] if self.action in self.serializers else self.serializers['default']

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
