from django.urls import path
from django.views.generic import ListView, DetailView
from .models import Player

urlpatterns = [
    # path('', ListView.as_view(model=Player), name='player_list'),
    # path('<int:pk>/', DetailView.as_view(model=Player), name='player_detail'),
]