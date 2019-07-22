from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Viewer



class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()
    cctvcode=forms.CharField(max_length=10)

    class Meta:

        model = User
        fields = ['username', 'email','cctvcode', 'password1', 'password2']

class BookingForm(forms.ModelForm):

    no_of_hours=forms.IntegerField()
    car_number=forms.CharField(max_length=10)
    class Meta:
        model = Viewer
        fields=['car_number','no_of_hours']





class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()
    class Meta:

        model = User
        fields = ['username', 'email']





class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile
        fields = ['image']
