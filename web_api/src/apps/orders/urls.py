from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('orders', views.OrderViewSet, 'orders')


urlpatterns = [
    path('', include(router.urls)),
]
