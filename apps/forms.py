from django.contrib.auth.forms import UserChangeForm

from .models import User


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'confirmed_password')
