from django import forms
from freelancer.models import CustomUser
from django.contrib.auth.forms import UserCreationForm , UserChangeForm

# Creation User form update
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')

# Editing User form update
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')