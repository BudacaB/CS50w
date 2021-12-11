from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Food(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_expenses")
    created = models.DateField(auto_now_add=True)
    amount = models.FloatField()

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bills_expenses")
    created = models.DateField(auto_now_add=True)
    amount = models.FloatField()

class Transport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transport_expenses")
    created = models.DateField(auto_now_add=True)
    amount = models.FloatField()

class Fun(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fun_expenses")
    created = models.DateField(auto_now_add=True)
    amount = models.FloatField()
