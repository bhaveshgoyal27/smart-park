from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
settings.AUTH_USER_MODEL
# Create your models here.
class UserProfileInfo(models.Model):
    #user = models.OneToOneField(User,on_delete=models.CASCADE)
    username = models.CharField(max_length=250, default='00')
    name = models.CharField(max_length=250, default='00')
    phno = models.BigIntegerField(default='00')
    password = models.CharField(max_length=1000,default='00')
    lat = models.FloatField(null=True, blank=True)
    log = models.FloatField(null=True, blank=True)
    max_cars = models.BigIntegerField(default='00')
    carsp = models.BigIntegerField(default='00')
    totalcarsp =models.BigIntegerField(default='00')
    def __str__(self):
        return self.username

class UserData(models.Model):
    username = models.CharField(max_length=100,unique=True,blank=True)
    name = models.CharField(max_length=100, unique=True, blank=True)
    carno = models.CharField(max_length=10, unique=True, blank=True)
    phno = models.IntegerField(null=True, blank= True)

    def __str__(self):
        return self.username