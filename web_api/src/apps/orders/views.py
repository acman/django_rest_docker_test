from rest_framework import viewsets

from .models import Order
from .permissions import AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly
from .serializers import OrderListSerializer, OrderCreateUpdateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializers = {
        'default': OrderListSerializer,
        'create': OrderCreateUpdateSerializer,
        'update': OrderCreateUpdateSerializer,
    }
    permission_classes = (AnonCreateAndRetrieveUpdateDeleteOwnerOrStaffOnly, )

    def get_serializer_class(self):
        """
        Return default if serializer for action not created.
        """
        return self.serializers[self.action] if self.action in self.serializers else self.serializers['default']

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
