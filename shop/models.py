from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.menu_item.name}"    


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
    max_length=20,
    choices=[
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ],
    default='Pending'
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"