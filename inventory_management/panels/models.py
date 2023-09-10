from django.apps import apps
from django.db import models
from django.contrib.auth import get_user_model
User= get_user_model()

CATEGORY = (
    ("Stationary", "Stationary"),
    ("Electronics", "Electronics"),
    ("Food", "Food"),
)


class Branch(models.Model):
    dealer_field = models.ForeignKey('Dealer', on_delete=models.CASCADE)
    name=models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    managers = models.ManyToManyField('BranchManager', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.city} Branch of {self.dealer_field.name}"
    
    def managers_as_string(self):
        return ", ".join([manager.name for manager in self.managers.all()])

class Product(models.Model):
    branch_field = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=50,choices=CATEGORY)
    unit_cost = models.IntegerField()

    def __str__(self):
        return self.name

class Dealer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    branches = models.ManyToManyField(Branch)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class BranchManager(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10)
    pan_number = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.product} ordered quantity {self.order_quantity}"

