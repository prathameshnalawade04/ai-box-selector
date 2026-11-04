from django.db import models
from django.contrib.auth.models import User

class Box(models.Model):
    name = models.CharField(max_length=100, unique=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, help_text="Internal length in cm")
    width = models.DecimalField(max_digits=8, decimal_places=2, help_text="Internal width in cm")
    height = models.DecimalField(max_digits=8, decimal_places=2, help_text="Internal height in cm")
    max_weight_capacity = models.DecimalField(max_digits=8, decimal_places=2, help_text="Max weight in kg")
    cost = models.DecimalField(max_digits=8, decimal_places=2, help_text="Cost in ₹")

    @property
    def volume(self):
        return self.length * self.width * self.height

    @property
    def max_dimension(self):
        return max(self.length, self.width, self.height)

    def __str__(self):
        return f"{self.name} - ₹{self.cost}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    length = models.DecimalField(max_digits=8, decimal_places=2)
    width = models.DecimalField(max_digits=8, decimal_places=2)
    height = models.DecimalField(max_digits=8, decimal_places=2)
    weight = models.DecimalField(max_digits=8, decimal_places=2, help_text="Weight in kg")

    @property
    def volume(self):
        return self.length * self.width * self.height

    @property
    def max_dimension(self):
        return max(self.length, self.width, self.height)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def total_weight(self):
        # Multiplies weight by quantity for each item and sums it up
        return sum(item.product.weight * item.quantity for item in self.items.all())
        
    @property
    def total_volume(self):
        # Multiplies volume by quantity for each item and sums it up
        return sum(item.product.volume * item.quantity for item in self.items.all())
        
    @property
    def max_item_dimension(self):
        # Finds the longest single dimension across all items in the order
        if not self.items.exists():
            return 0
        return max(item.product.max_dimension for item in self.items.all())

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"