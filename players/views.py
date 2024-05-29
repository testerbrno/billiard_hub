from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        referer = self.request.META.get('HTTP_REFERER')
        messages.error(self.request, "Login failed. Please try again.")
        return HttpResponseRedirect(referer)
