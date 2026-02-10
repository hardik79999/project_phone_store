from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)  # Unique slug required
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class Specification(models.Model):
    product = models.ForeignKey(Product, related_name='specs', on_delete=models.CASCADE)
    key_name = models.CharField(max_length=100)  # e.g., "RAM"
    value = models.CharField(max_length=100)     # e.g., "8GB"

    def __str__(self):
        return f"{self.key_name}: {self.value}"
    # --- Is code ko file ke end mein paste karo ---
from django.contrib.auth.models import User

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    # Total price nikalne ka logic
    def get_total_price(self):
        return self.quantity * self.product.price