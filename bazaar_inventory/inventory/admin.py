from django.contrib import admin
from .models import Product, Store, Inventory, StockMovement, AuditLog


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'unit_price', 'created_at', 'updated_at')
    search_fields = ('name', 'sku', 'description')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_number', 'is_active', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'product', 'quantity', 'last_updated')
    search_fields = ('store__name', 'product__name', 'product__sku')
    list_filter = ('store', 'last_updated')
    readonly_fields = ('last_updated',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'store', 'product', 'movement_type', 'quantity', 'reference_number')
    search_fields = ('store__name', 'product__name', 'product__sku', 'reference_number')
    list_filter = ('movement_type', 'store', 'timestamp')
    readonly_fields = ('created_at',)
    date_hierarchy = 'timestamp'


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'entity_type', 'entity_id', 'user', 'ip_address')
    search_fields = ('action', 'entity_id', 'user', 'details')
    list_filter = ('action', 'entity_type', 'timestamp')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'