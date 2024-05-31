
from django.urls import path
from app1 import views

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/', views.LoginPage,name='login'),
    path('home/', views.Homepage,name='home'),
    path('logout/',views.LoginPage,name='logout'),
    path('create_server/', views.create_server, name='create_server'),
    path('servers/<int:pk>/', views.server_detail, name='server_detail'),
]