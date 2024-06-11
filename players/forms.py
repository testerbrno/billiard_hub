from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Player

class PlayerCreationForm(UserCreationForm):
    class Meta:
        model = Player
        fields = ['username', 'email', 'password1', 'password2']

class PlayerUpdateForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'email']

# if i will be in need of disabling to change username
    # def __init__(self, *args, **kwargs):
    #     super(PlayerUpdateForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].disabled = True