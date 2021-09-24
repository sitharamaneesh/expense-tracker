from django.db import models
from django.contrib.auth.models import User
from django.http import request

class expense(models.Model):
    user=models.CharField(max_length=20,default="null")
    expense=models.CharField(max_length=20)
    amount=models.DecimalField(max_digits=7,decimal_places=2)
    
    def __str__(self) :
        return self.user

class balance(models.Model):
    user=models.CharField(max_length=20,default="null")
    deposit=models.DecimalField(max_digits=7,decimal_places=2)
    def __str__(self) :
        return self.user

# Create your models here.
