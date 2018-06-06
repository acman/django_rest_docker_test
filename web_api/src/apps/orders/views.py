import json

from rest_framework import viewsets, serializers, status
from rest_framework.response import Response

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
                /orders/?created_date__range=["2018-06-03","2018-06-04"]

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
        'partial_update': OrderCreateUpdatePatchSerializer,
    }
    permission_classes = (AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly, )

    def _ckeck_status(self, instance):
        if instance.status != Order.NEW:
            raise serializers.ValidationError('Order can not be modified.')

    def _get_filters(self):
        filters = {}
        created_date_range = self.request.GET.get('created_date__range')
        if created_date_range:
            date_min, date_max = json.loads(created_date_range)
            filters['created_date__range'] = [date_min, date_max]

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self._ckeck_status(instance)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self._ckeck_status(instance)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
