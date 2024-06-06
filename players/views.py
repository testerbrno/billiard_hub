from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from .models import Player

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
            print(f"Error during search: {e}")
            return JsonResponse({'error': 'An error occurred during search'}, status=500)

        results = [{'label': player.username, 'value': player.username, 'id': player.pk} for player in players]
        return JsonResponse(results, safe=False)
