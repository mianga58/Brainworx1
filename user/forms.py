from django import forms
from django.contrib.auth.models import User
from accounts.forms import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User

        fields = ['username', 'email', 'password']
