from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.views.generic import (
    DetailView, 
    TemplateView, 
)

from .forms import UserRegisterForm
from .models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'''Account created successfully. You can now login using these credentials.''')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

def logout_view(request):
    if User.is_authenticated:
        logout(request)
        messages.success(request, f'Logged out successfully.')
    return redirect('index')

class UserProfileView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile.html'

class OwnProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile_self.html'