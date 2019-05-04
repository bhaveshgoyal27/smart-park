"""from django.db import models

# Create your models here.
class details(models.Model):
    name=models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    password= models.CharField(max_length=1000)
    phno = models.BigIntegerField()
    email = models.CharField(max_length=250)"""
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    phno = models.BigIntegerField()
    email = models.CharField(max_length=250)
    def __str__(self):
        return self.user.username