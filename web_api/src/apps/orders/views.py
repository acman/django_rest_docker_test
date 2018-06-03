from rest_framework import viewsets

from .models import Order
from .permissions import AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly
from .serializers import OrderListSerializer, OrderCreateUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': OrderListSerializer,
        'create': OrderCreateUpdateSerializer,
        'update': OrderCreateUpdateSerializer,
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
