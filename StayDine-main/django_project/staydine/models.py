from django.db import models

# Create your models here.
class Highlights(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(max_length=1000)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name=models.CharField(max_length=122)
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=10)
    desc=models.TextField()
    date=models.DateField()
    def _str_(self):
        return self.name
    
class Dining(models.Model):
    email = models.EmailField(max_length=254)
    item_no = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.email} - Item: {self.item_no} - Qty: {self.quantity}"
    
# models.py

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=1000)
    total_rooms = models.PositiveIntegerField(default=100)  # default is 100

    def __str__(self):
        return self.name


class BedType(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    email = models.EmailField(primary_key=True)
    classic_rooms = models.PositiveIntegerField(default=0)
    premium_rooms = models.PositiveIntegerField(default=0)
    suite_rooms = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.email} from {self.start_date} to {self.end_date}"

    
class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('Pizza', 'Pizza'),
        ('Beverages', 'Beverages'),
        ('South Indian', 'South Indian'),
        ('Starters', 'Starters'),
        ('Dessert', 'Dessert'),
        ('North Indian', 'North Indian'),
    ]
    
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES,default='Beverages')
    description = models.TextField()
    image_url = models.URLField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
