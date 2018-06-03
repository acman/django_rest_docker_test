from django.contrib import admin

from .models import Order, OrderProductMembership


class OrderProductMembershipInline(admin.TabularInline):
    model = OrderProductMembership
    raw_id_fields = ('product', )
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'total_price', 'status')
    list_filter = ('status', )
    list_display_links = ('id', 'client')
    search_fields = ('id', )
    list_editable = ('status', )
    inlines = (OrderProductMembershipInline, )
