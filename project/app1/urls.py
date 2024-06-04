
from django.urls import path
from app1 import views
from .views import create_server

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/', views.LoginPage,name='loginn'),
    path('home/', views.Homepage,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path('create-server/', create_server, name='create_server'),
]