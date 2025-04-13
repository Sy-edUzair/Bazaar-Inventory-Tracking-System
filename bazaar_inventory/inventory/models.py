from django.db import models
import uuid
from django.core.validators import MinValueValidator
from django.utils import timezone

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Store(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['store', 'product']
        verbose_name_plural = 'Inventories'

    def __str__(self):
        return f"{self.product.name} at {self.store.name}: {self.quantity} units"

class StockMovementType(models.TextChoices):
    STOCK_IN = 'STOCK_IN', 'Stock In'
    SALE = 'SALE', 'Sale'
    MANUAL_REMOVAL = 'MANUAL_REMOVAL', 'Manual Removal'

class StockMovement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='stock_movements')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=StockMovementType.choices)
    quantity = models.PositiveIntegerField()
    reference_number = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity} units)"

class AuditLog(models.Model):
    #Audit log for tracking all actions in the system.
    #This will be important in Stage 3 for compliance and debugging.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=50)
    entity_id = models.CharField(max_length=50)
    user = models.CharField(max_length=100, blank=True)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} {self.entity_type} at {self.timestamp}"