from django.db import models

from django.contrib.auth.models import User

from PIL import Image
import geocoder





class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    g = geocoder.ip('me')
    lat = models.FloatField(default=g.latlng[0])
    lng = models.FloatField(default=g.latlng[1])
    phno=models.IntegerField(default='0')
    cctvcode=models.CharField(max_length=10, default=0)
    photage = models.ImageField(default='qa.png', upload_to='cctv')
    carsp = models.IntegerField(default=0)
    cost = models.IntegerField(default=40)
    choice= models.CharField(max_length=1,default=0)

    def __str__(self):
        return f'{self.user.username} Profile'



    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.image.path)
        img1=Image.open(self.photage.path)

        if img.height > 300 or img.width > 300:

            output_size = (300, 300)

            img.thumbnail(output_size)

            img.save(self.image.path)

        if img1.height > 300 or img1.width > 300:

            output_size = (224, 224)

            img1.thumbnail(output_size)

            img1.save(self.photage.path)

class Viewer(models.Model):
    car_number = models.CharField(max_length=10, default=0)
    no_of_hours=models.IntegerField(default=0)