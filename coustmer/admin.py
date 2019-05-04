"""from django.contrib import admin
from .models import coustmer
# Register your models here.
admin.site.register(coustmer)"""
from django.contrib import admin
from coustmer.models import UserProfileInfo, User
# Register your models here.
admin.site.register(UserProfileInfo)