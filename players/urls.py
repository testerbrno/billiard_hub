from django.urls import path
from django.views.generic import ListView, DetailView
from .models import Player
from .views import PlayerSearchView

urlpatterns = [
    path('', ListView.as_view(model=Player, template_name="./list/player_list.html"), name='player_list'),
    path('<int:pk>/', DetailView.as_view(model=Player, template_name="./detail/player_detail.html"), name='player_detail'),
    path('search/', PlayerSearchView.as_view(), name='player_search'),
]