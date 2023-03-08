from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Restaurant(models.Model):
    name=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    status=models.BooleanField(default=True)
    
    def __str__(self):
        
        return self.name
    
    
class Menu(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    dish_name=models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time_taken=models.IntegerField(default=0)
    
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    def get_total_price(self):
            total_price = sum(item.total_price for item in self.items.all())
            return total_price
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    dish_id=models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.FloatField(default=0)
    dish_name=models.CharField(max_length=200,default='TestDishName')
    @property
    def total_price(self):
        return self.dish_id.price * self.quantity
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dish_name=models.CharField(max_length=200)
    
    
    
    
    
    
    

    

