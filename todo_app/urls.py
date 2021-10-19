from django.http.response import HttpResponse
from django.urls import path 
from . import views 

urlpatterns = [ 
    path('', views.login_page, name="login"),
    path('index', views.index, name='index'),
    path('home/<name>', views.home, name='home'),
    path('delete_stuff/<list_name>', views.delete_stuff, name="delete_stuff"),
    path('add_stuff/<list_name>', views.add_stuff, name="add_stuff"),
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('signup_user', views.signup_user, name="signup_user"),
]