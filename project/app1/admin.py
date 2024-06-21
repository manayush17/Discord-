from django.contrib import admin
from.models import Server, Membership,Channel,FriendRequest

admin.site.register(Server)
admin.site.register(Membership)
admin.site.register(Channel)
admin.site.register(FriendRequest)