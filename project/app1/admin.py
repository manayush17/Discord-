from django.contrib import admin
from .models import User
from.models import Server
from .models import Membership

admin.site.register(User)
admin.site.register(Server)
admin.site.register(Membership)