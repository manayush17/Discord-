
from django.urls import path
from app1 import views
from .views import create_server
from .views import create_server, server_detail ,list_servers ,join_server

urlpatterns = [
    path('',views.SignupPage,name='signup'),
    path('login/', views.LoginPage,name='loginn'),
    path('home/', views.Homepage,name='home'),
    path('logout/',views.logout_view,name='logout'),
    path('create-server/', create_server, name='create_server'),
    path('server/<int:server_id>/', server_detail, name='server_detail'),
    path('server/', list_servers, name='list_servers'),
    path('server/<int:server_id>/join/', join_server, name='join_server'),

]