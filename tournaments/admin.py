from django.contrib import admin
from tournaments.models import Tournament, Round, Match

# Register your models here.
admin.site.register([Tournament, Round, Match])