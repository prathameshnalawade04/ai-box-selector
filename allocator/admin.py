from django.contrib import admin
from .models import Box, Product, Order, OrderItem

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'max_weight_capacity', 'length', 'width', 'height', 'display_volume')
    list_display_links = ('name',)
    list_filter = ('cost',)
    search_fields = ('name',)

    def display_volume(self, obj):
        return obj.volume
    display_volume.short_description = 'Volume (cm³)'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'length', 'width', 'height', 'display_volume')
    list_display_links = ('name',)
    list_filter = ('weight',)
    search_fields = ('name',)

    def display_volume(self, obj):
        return obj.volume
    display_volume.short_description = 'Volume (cm³)'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Shows one empty row by default to add a new product


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'created_at', 'display_total_weight', 'display_total_volume')
    list_display_links = ('order_number',)
    list_filter = ('created_at', 'user')
    search_fields = ('order_number',)
    inlines = [OrderItemInline]

    def display_total_weight(self, obj):
        return f"{obj.total_weight} kg"
    display_total_weight.short_description = 'Total Weight'

    def display_total_volume(self, obj):
        return obj.total_volume
    display_total_volume.short_description = 'Total Volume'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    list_display_links = ('id',)
    list_filter = ('order__order_number', 'product')
    search_fields = ('order__order_number', 'product__name')