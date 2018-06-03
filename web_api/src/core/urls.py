from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Orders CRUD')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', schema_view),
    path('', include(('orders.urls', 'orders'), namespace='orders')),
]
