from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,BookingForm
from .models import Profile
from math import cos, asin, sqrt
from django.http import HttpResponse
import geocoder

def base(request):
    return render(request,'user/base.html')


def book(request,profile_id):
    a=Profile.objects.filter(id=profile_id).first()
    return render(request, 'user/details.html', {'details': a})


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295     
    a = 0.5 - cos((lat2 - lat1) * p)/2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    return 12742 * asin(sqrt(a))

def get_loc(request):
    if request.method == 'POST':
        b_form=BookingForm(request.POST)
        if b_form.is_valid():
            b_form.save()
            car_number = b_form.cleaned_data.get('car_number')
            in_time = b_form.cleaned_data.get('in_time')
            out_time = b_form.cleaned_data.get('out_time')
            time=out_time - in_time
            if time/3600 == time//3600:
                time=time//3600
            else:
                time=time//3600
            time+=1
            det=Profile.objects.all()
            g=geocoder.ip('me')
            a=g.latlng[0]
            b=g.latlng[1]
            d={}
            m=[]
            for i in det:
                if distance(i.lat,i.lng,a,b)<=5:
                    d[i]=distance(i.lat,i.lng,a,b)
            if d :
                 return render(request, 'user/detail.html', {'detail': d,'car':car_number,'time':time})
            else:
                messages.success(request, f'THERE ARE NO PARKING SPOTS NEAR YOU AT THE TIME')
                return redirect('base')
        else:
            return HttpResponse("bh")
    else:
        b_form = BookingForm()
    context = {
        'b_form': b_form
    }
    return render(request, 'user/get_loc.html', context)
    """else:
            return HttpResponse("bh")
        time=out_time - in_time
        if time/3600 == time//3600:
            time=time//3600
        else:
            time=time//3600
            time+=1
        det=Profile.objects.all()
        g=geocoder.ip('me')
        a=g.latlng[0]
        b=g.latlng[1]
        d={}
        m=[]
        for i in det:
            if distance(i.lat,i.lng,a,b)<=5:
                d[i]=distance(i.lat,i.lng,a,b)
        if d :
             return render(request, 'user/detail.html', {'detail': d,'car':car_number,'time':time})
        else:
            messages.success(request, f'THERE ARE NO PARKING SPOTS NEAR YOU AT THE TIME')
            return redirect('base')
    else:
        b_form = BookingForm()
    context = {
        'b_form': b_form
    }
    return render(request, 'user/get_loc.html', context)"""
    """det=Profile.objects.all()
    g=geocoder.ip('me')
    a=g.latlng[0]
    b=g.latlng[1]
    d={}
    m=[]
    for i in det:
        if distance(i.lat,i.lng,a,b)<=5:
            d[i]=distance(i.lat,i.lng,a,b)
    if d :
         return render(request, 'user/detail.html', {'detail': d})
    else:
        return HttpResponse ("THERE ARE NO PARKING SPOTS NEAR YOU ")
    return render(request, 'user/detail.html', {'detail': d})"""



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})





@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user/profile.html', context)