from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


# Create custom user creation form
# CREDIT: Pyplane
# URL: https://www.youtube.com/watch?v=1BeZxMbSZNI
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = "__all__"
