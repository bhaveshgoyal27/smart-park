from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,ProfileUpdateForm,BookingForm
from .models import Profile
from math import cos, asin, sqrt
from django.http import HttpResponse
import geocoder
import requests
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
import numpy as np
import keras
import cv2
import tensorflow as tf
from keras import backend
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense, Flatten
from keras.optimizers import Adam
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import *
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
import matplotlib.pyplot as plt
#%matplotlib inline
#global graph
#graph=tf.get_default_graph()
import smtplib
from email.message import EmailMessage

email_id=os.environ.get('USER_ID')
email_pass=os.environ.get('USER_PASS')

def base(request):
    return render(request,'user/base.html')


def book(request,profile_id):
    if request.method == 'POST':
        b_form=BookingForm(request.POST)
        if b_form.is_valid():
            b_form.save()
            car_number = b_form.cleaned_data.get('car_number')
            time = b_form.cleaned_data.get('no_of_hours')
            a=Profile.objects.filter(id=profile_id).first()
            c=a.user
            b=User.objects.filter(username=c).first()
            msg=EmailMessage()
            d=b.email
            msg['Subject']='PARKSPOT'
            msg['From']=email_id
            msg['To']=d
            msg.set_content('NEW BOOKING FOR YOU')
            msg.add_alternative("""\
                <!DOCTYPE html>
                <html>
                <body>
                <h1 style"color:Red;">CAR NUMBER {car_number} is going to park his car for 
                {no_of_hours} hours.</h1>
                </body>
                </html>
                                """, subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
                smtp.login(email_id,email_pass)
                smtp.send_message(msg)  
            return render(request, 'user/details.html', {'details': a})
        else:
            b_form = BookingForm()
            context = {'b_form': b_form}
            return render(request, 'user/get_loc.html', context)
    else:
        b_form = BookingForm()
        context = {'b_form': b_form}
        return render(request, 'user/get_loc.html', context)


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def check(x):
    CNN=keras.applications.vgg16.VGG16()
    model=Sequential()
    for capa in CNN.layers:
        model.add(capa)
    for layer in model.layers:
        layer.trainable=False
    model.add(Dense(2,activation='softmax'))
    model.load_weights("C:\\Users\\bhavs\\Desktop\\final_model_22_july_for_sure.h5")
    #test='C:\\Users\\bhavs\\Desktop\\qa.jpg'
    test=cv2.imread(x)
    image=test
    stepSize = 10
    c=1
    (w_width, w_height) = (10, 15) # window size
    for x in range(0, image.shape[1] - w_width , stepSize):
        for y in range(0, image.shape[0] - w_height, stepSize):
            window = image[x:x + w_width, y:y + w_height, :]
            window=cv2.resize(window,(224,224))
            window=np.reshape(window,[1,224,224,3])
            a=model.predict(window)
            b=np.round(a[0][0])
            if b==1:
                c+=1
    return c

def get_loc(request):
    g=geocoder.ip('me')
    a=g.latlng[0]
    b=g.latlng[1]
    d={}
    m=[]
    det=Profile.objects.all()
    for i in det:
        if (distance(i.lat,i.lng,a,b)<=5 and check(i.photage.path)<10):
            d[i]=distance(i.lat,i.lng,a,b)
    if d :
        return render(request, 'user/parkingspots.html', {'detail': d})
    else:
        messages.success(request, f'THERE ARE NO PARKING SPOTS NEAR YOU AT THE TIME')
        return redirect('base')

"""def get_loc(request):
    if request.method == 'POST':
        b_form=BookingForm(request.POST)
        if b_form.is_valid():
            b_form.save()
            car_number = b_form.cleaned_data.get('car_number')
            time = b_form.cleaned_data.get('no_of_hours')
            det=Profile.objects.all()
            g=geocoder.ip('me')
            a=g.latlng[0]
            b=g.latlng[1]
            d={}
            m=[]
            for i in det:
            	if (distance(i.lat,i.lng,a,b)<=5 and check(i.photage.path)>=0.5):
                	d[i]=distance(i.lat,i.lng,a,b)
            if d :
                return render(request, 'user/parkingspots.html', {'detail': d,'car':car_number,'time':time})
                #return render(request, 'user/detail.html', {'detail': d,'car':car_number,'time':time})
            else:
                messages.success(request, f'THERE ARE NO PARKING SPOTS NEAR YOU AT THE TIME')
                return redirect('base')
        else:
            b_form = BookingForm()
            context = {'b_form': b_form}
            return render(request, 'user/get_loc.html', context)
    else:
        b_form = BookingForm()
    context = {
        'b_form': b_form
    }
    return render(request, 'user/get_loc.html', context)
   """ 

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            emailid = form.cleaned_data.get('email')
            messages.success(request, f'Your account has been created! You are now able to log in')
            msg=EmailMessage()

            msg['Subject']='PARKSPOT'
            msg['From']=email_id
            msg['To']=emailid
            msg.set_content('qwertyuibn')
            msg.add_alternative("""\
                <!DOCTYPE html>
                <html>
                <body>
                <h1 style"color:Blue;">THANK YOU FOR REGISTERING YOUR PARKING SPOT WITH US.</h1>
                <h3 style"color:Blue;">We hope you enjoy doing business with us.</h3>
                </body>
                </html>
                                """, subtype='html')
            with smtplib.SMTP_SSL('smtp.gmail.com',465)as smtp:
                smtp.login(email_id,email_pass)
                smtp.send_message(msg)  
            return redirect('login')
        else:
            form = UserRegisterForm()
            return render(request, 'user/register.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})
    #return render(request, 'user/r.html',{'form':form})





@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if p_form.is_valid():

            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'p_form': p_form
    }
    return render(request, 'user/profile1.html', context)