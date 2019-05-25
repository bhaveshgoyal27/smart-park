from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import UserProfileInfo,UserData
import geocoder


from django.template import loader
#from .urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    template=loader.get_template('index.html')
    return HttpResponse(template.render(request))


def details(request,name):
    a=UserProfileInfo.objects.all()
    for i in a:
        if i.name==name:
            i.carsp+=1
            i.save()
            #return HttpResponse("CLICK TO VIEW THE FULL MAP!!")
            return render(request, 'details.html', {'details': i})

def location(lat,log,lat1,og1):
    a=lat1-lat
    a*=111.660
    b=og1-log
    b*=111.66
    c=a*a+b*b
    return c**0.5

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    #return HttpResponse("YOU'VE HAVE SUCESSFULLY LOGGED OUT")

def get_loc(request):
    loc=UserProfileInfo.objects.all()
    g = geocoder.ip('me')
    a= g.latlng[0]
    b= g.latlng[1]
    d=dict()
    for i in loc:
        if location(i.lat,i.log,a,b)<=15:
           d[i.name]=[location(i.lat,i.log,a,b),i.name]
    if d :
         html=''
         for i in d :
            url='/coustmer/'+ i + '/'
            html+= '<a href=' + url +'>' + d[i][1] + '</a><br>'
         return HttpResponse(html)
    else:
        return HttpResponse ("THERE ARE NO PARKING SPOTS NEAR YOU ")


def register(request) :
    if request.method=='POST':
        g = geocoder.ip('me')
        detail=UserProfileInfo(username=request.POST.get('Username'),password=request.POST.get('password'),name=request.POST.get('Name'),max_cars=request.POST.get('Name'),phno=request.POST.get('Phone Number'),lat=g.latlng[0],log=g.latlng[1])
        detail.save()
        user = authenticate(username=request.POST.get('Username'), password=request.POST.get('password'))
        login(request, user)
        return render(request, 'detail.html', {'detail': detail})
    else:
        return render(request, 'reg.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        return HttpResponse(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                details = UserProfileInfo.objects.filter(user=request.user)
                return render(request, 'detail.html', {'detail': details})
            else:
                return render(request, 'login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    return render(request, 'login.html')

def coustmer_register(request):
    if request.method=='POST':
        detail=UserData(username=request.POST.get('Username'),password=request.POST.get('password'),carno=request.POST.get('carno'),phno=request.POST.get('Phone Number'))
        detail.save()
        user = authenticate(username=request.POST.get('Username'), password=request.POST.get('password'))
        login(request, user)
        return render(request, 'detail.html', {'detail': detail})
    else:
        return render(request, 'register.html')