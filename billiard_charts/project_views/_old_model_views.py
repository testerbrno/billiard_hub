from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import Http404
from players.models import Player
from tournaments.models import Tournament, Match, Round

class ByUserQuerysetMixin:
    def get_queryset(self):
        model_name = self.kwargs.get('model')
        model_class = globals().get(model_name)
        if model_class:
            match model_name:
                case "Player":
                    return model_class.objects.filter(pk=self.request.user.pk)
                case "Tournament" | "Match" | "Round":
                    return model_class.objects.filter(created_by=self.request.user.pk)
        return super().get_queryset()

class ModelQuerysetMixin:
    def get_queryset(self):
        model_name = self.kwargs.get('model')
        model_class = globals().get(model_name)
        queryset = model_class.objects.all() if model_class else None
        return queryset

class ModelListView(ModelQuerysetMixin, ListView):
    pass

class ModelDetailView(LoginRequiredMixin, ByUserQuerysetMixin, DetailView):
    def get_object(self):
        model_name = self.kwargs.get('model')
        model_class = globals().get(model_name)
        
        if not model_class:
            return {'error_message': 'Model not found'}
        
        requested_object = model_class.objects.filter(pk=self.kwargs['pk']).first()
        
        if not requested_object:
            return {'error_message': 'Object not found'}
        
        requesting_user = self.request.user
        
        match model_name:
            case "Player":
                if requested_object.pk != requesting_user.pk:
                    return {'error_message': 'You are not allowed to view this.'}
            case "Tournament" | "Round" | "Match":
                if requested_object.created_by != requesting_user and requesting_user not in requested_object.assigned_players.all():
                    return {'error_message': 'You are not allowed to view this.'}
        
        return requested_object

class ModelDeleteView(LoginRequiredMixin, ModelQuerysetMixin, DeleteView):
    success_url = reverse_lazy('home'),

class ModelUpdateView(LoginRequiredMixin, ModelQuerysetMixin, UpdateView):
    pass
