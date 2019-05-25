from django.conf.urls import url
from . import views
# SET THE NAMESPACE!
app_name = 'coustmer'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^get_loc/$',views.get_loc,name='get_loc'),
    url(r'^(?P<name>[a-zA-Z]+)/$', views.details, name='details'),
]