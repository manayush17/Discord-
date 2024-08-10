from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='loginn'),
    path('logout/', views.logout_view, name='logout'),
    path('create_server/', views.create_server, name='create_server'),
    path('servers/<int:server_id>/', views.server_detail, name='server_detail'),
    path('list_servers/', views.list_servers, name='list_servers'),
    path('join_server/<int:server_id>/', views.join_server, name='join_server'),
    path('send_friend_request/<int:receiver_id>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('friends_list/', views.friends_list, name='friends_list'),
    path('servers/<int:server_id>/channels/<int:channel_id>/', views.channel_detail, name='channel_detail'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),
    path('servers/<int:server_id>/create_invitation/', views.create_invitation, name='create_invitation'),
    path('invite/<str:code>/', views.join_via_invitation, name='join_via_invitation'),
    path('confirm_join/<str:code>/', views.confirm_join_server, name='confirm_join_server'),
    path('servers/<int:server_id>/promote/<int:user_id>/', views.promote_to_moderator, name='promote_to_moderator'),
    path('servers/<int:server_id>/demote/<int:user_id>/', views.demote_to_member, name='demote_to_member'),
    path('servers/<int:server_id>/remove/<int:user_id>/', views.remove_member, name='remove_member'),
    path('server/<int:server_id>/channel/<int:channel_id>/grant/<int:user_id>/', views.grant_channel_access, name='grant_channel_access'),
    path('server/<int:server_id>/channel/<int:channel_id>/restrict/<int:user_id>/', views.restrict_channel_access, name='restrict_channel_access'),
    path('upload_file/', views.upload_file, name='upload_file'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

