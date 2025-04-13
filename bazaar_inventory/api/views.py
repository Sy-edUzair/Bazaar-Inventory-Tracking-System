from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from inventory.models import *
from .serializers import *
from django.db.models import F
from django.db import transaction


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'sku', 'description']
    filterset_fields = ['sku']


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'location']
    filterset_fields = ['is_active']


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'product']

    @action(detail=False, methods=['get'])
    def by_store(self, request):
        store_id = request.query_params.get('store_id')
        if not store_id:
            return Response(
                {"error": "store_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.queryset.filter(store_id=store_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-timestamp')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'product', 'movement_type', 'timestamp']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CreateStockMovementSerializer
        return StockMovementSerializer
    
    @transaction.atomic
    def perform_create(self, serializer):
        movement = serializer.save()
        inventory, created = Inventory.objects.get_or_create(
            store=movement.store,
            product=movement.product,
            defaults={'quantity': 0}
        )
        
        if movement.movement_type == StockMovementType.STOCK_IN:
            inventory.quantity = F('quantity') + movement.quantity
        else:
            inventory.quantity = F('quantity') - movement.quantity
        
        inventory.save()
        inventory.refresh_from_db()
        AuditLog.objects.create(
            action=f"STOCK_{movement.movement_type}",
            entity_type="StockMovement",
            entity_id=str(movement.id),
            user=self.request.user.username if hasattr(self.request, 'user') else "system",
            details={
                "product_id": str(movement.product.id),
                "store_id": str(movement.store.id),
                "quantity": movement.quantity,
                "new_inventory_level": inventory.quantity
            }
        )


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['action', 'entity_type', 'entity_id', 'timestamp']