from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Viewer



class UserRegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User
        fields = ['username', 'email', 'password1', 'password2']

class BookingForm(forms.ModelForm):

    in_time=forms.IntegerField()
    out_time=forms.IntegerField()
    car_number=forms.CharField(max_length=10)
    class Meta:
        model = Viewer
        fields=['car_number','in_time','out_time']





class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    class Meta:

        model = User
        fields = ['username', 'email']





class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = Profile
        fields = ['image']
