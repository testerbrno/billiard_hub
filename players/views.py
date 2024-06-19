from django.views import View
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Player
from .forms import PlayerCreationForm, PlayerUpdateForm

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        referer = self.request.META.get('HTTP_REFERER')
        messages.error(self.request, "Login failed. Please try again.")
        return HttpResponseRedirect(referer)

class PlayerSearchView(View):
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('term', '')
        if len(search_term) < 3:
            return JsonResponse({'players': []})

        try:
            players = (Player.objects.filter(username__icontains=search_term) | Player.objects.filter(email__icontains=search_term))[:10]
        except Exception as e:
            return JsonResponse({'error': 'An error occurred during search'}, status=500)

        results = [{'label': player.username, 'value': player.username, 'id': player.pk} for player in players]
        return JsonResponse(results, safe=False)

class PlayerCreateView(CreateView):
        model = Player
        form_class = PlayerCreationForm
        success_url = reverse_lazy('player_list')
        
class PlayerUpdateView(UpdateView):
        model = Player
        form_class = PlayerUpdateForm
        success_url = reverse_lazy('player_list')