from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'inventory', InventoryViewSet)
router.register(r'stock-movements', StockMovementViewSet)
router.register(r'audit-logs', AuditLogViewSet)

urlpatterns = [
     path('', include(router.urls)),
]