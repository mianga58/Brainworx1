from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from accounts.forms import CustomUserCreationForm


def register_view(request):
    form = CustomUserCreationForm()
    print(form)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Successfully registered')
            return redirect(reverse('register'))
    return render(request, 'user/index_user.html', {'form': form})

