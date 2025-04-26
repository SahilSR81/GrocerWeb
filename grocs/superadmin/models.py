from django.db import models
from web.models import *



# Create your models here.
class Product(models.Model):
    pname = models.CharField(max_length=255)
    pprice = models.IntegerField()
    psellprice = models.IntegerField()
    pdiscount = models.IntegerField()
    pimage= models.ImageField(upload_to='product', default = '', blank=True)
    category = models.ForeignKey('category',on_delete=models.CASCADE,default=1)
    description= models.TextField()

class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    status = models.BooleanField(default=1)

    
class Cart(models.Model):
    customer = models.ForeignKey('web.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True)
    fruit = models.ForeignKey('Fruit', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    total_amt = models.IntegerField()
    status = models.BooleanField(default=1)
    is_wishlist = models.BooleanField(default=False)
        
class Meta:
    unique_together = ('customer', 'product', 'is_wishlist')
    
class Fruit(models.Model):
    fname = models.CharField(max_length=255)
    fprice = models.IntegerField()
    fsellprice = models.IntegerField()
    fdiscount = models.IntegerField()
    fimage= models.ImageField(upload_to='product', default = '', blank=True)
    menus = models.ForeignKey('menus',on_delete=models.CASCADE,default=1)
    fdescription= models.TextField()


class Menus(models.Model):
    cato_name = models.CharField(max_length=255)
    status = models.BooleanField(default=1)



class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

from django.db import models
from web.models import Customer

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # address = models.TextField()
    # total_amount = models.IntegerField()
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    # created_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()  # ✅ THIS MUST EXIST
    city = models.CharField(max_length=255, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(
        max_length=20, 
        choices=[('COD', 'Cash on Delivery'), ('Online', 'Online Payment')],
        default='COD' )
    status = models.CharField(max_length=20, default='Pending') # default value
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    fruit = models.ForeignKey(Fruit, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.get_product_name()} x {self.quantity}"

    def get_product_name(self):
        if self.product:
            return self.product.pname
        elif self.fruit:
            return self.fruit.fname
        return "N/A"

    def get_product_image(self):
        if self.product and self.product.pimage:
            return self.product.pimage.url
        elif self.fruit and self.fruit.fimage:
            return self.fruit.fimage.url
        return ""