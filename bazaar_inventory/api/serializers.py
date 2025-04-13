from rest_framework import serializers
from inventory.models import Product, Store, Inventory, StockMovement, AuditLog

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_sku = serializers.ReadOnlyField(source='product.sku')
    store_name = serializers.ReadOnlyField(source='store.name')
    
    class Meta:
        model = Inventory
        fields = ['id', 'store', 'store_name', 'product', 'product_name', 
                  'product_sku', 'quantity', 'last_updated']


class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    store_name = serializers.ReadOnlyField(source='store.name')
    
    class Meta:
        model = StockMovement
        fields = ['id', 'store', 'store_name', 'product', 'product_name', 
                  'movement_type', 'quantity', 'reference_number', 
                  'notes', 'timestamp', 'created_at']

class CreateStockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['store', 'product', 'movement_type', 'quantity', 
                 'reference_number', 'notes']
        
    def validate(self, data):
        #Check that stock levels don't go negative for sales or removals.
        if data['movement_type'] in ['SALE', 'MANUAL_REMOVAL']:
            try:
                inventory = Inventory.objects.get(
                    store=data['store'], 
                    product=data['product']
                )
                if inventory.quantity < data['quantity']:
                    raise serializers.ValidationError(
                        f"Insufficient stock. Current quantity: {inventory.quantity}"
                    )
            except Inventory.DoesNotExist:
                raise serializers.ValidationError("No inventory exists for this product in this store")
        
        return data

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]  