from django.db import models

# Create your models here

class Admin(models.Model):
    user_name=models.CharField(max_length=10)
    user_passwd=models.CharField(max_length=10)

class Expense(models.Model):
    name=models.CharField(max_length=30)
    dt=models.CharField(max_length=20)
    amount=models.FloatField()