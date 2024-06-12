from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='loginn'),
    path('logout/', views.logout_view, name='logout'),
    path('create_server/', views.create_server, name='create_server'),
    path('servers/<int:server_id>/', views.server_detail, name='server_detail'),
    path('list_servers/', views.list_servers, name='list_servers'),
    path('join_server/<int:server_id>/', views.join_server, name='join_server'),
     path('server/<int:server_id>/channel/<int:channel_id>/', views.channel_detail, name='channel_detail'),
]
