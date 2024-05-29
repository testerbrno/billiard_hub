from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from players.models import Player

# Register your models here.
admin.site.register(Player, UserAdmin)
