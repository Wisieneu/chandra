from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import (
    ListView,

)

from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from main.models import Post


def signup_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Account created successfully. You can now login using these credentials.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def logout_view(request):
    if User.is_authenticated:
        logout(request)
        messages.success(request, f'Logged out successfully.')
    return redirect('index')

@login_required
def profile_redirect(request):
    slug = request.user.username
    return redirect(f'/profile/{slug}')


class UserProfileView(ListView):
    model = Post
    context_object_name = 'user_posts'
    template_name = 'users/profile.html'
    paginate_by = 5
    ordering = ['-date_posted']
    
    def get_queryset(self, *args, **kwargs):    
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(author__profile__slug=self.kwargs['slug'])
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile'] = get_object_or_404(Profile, slug=self.kwargs['slug'])
        return context

@login_required
def settings_view(request):
    if request.method == 'POST':
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_update_form = UserUpdateForm(
            request.POST, instance=request.user)
        if profile_update_form.is_valid() and user_update_form.is_valid():
            profile_update_form.save()
            user_update_form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('settings')
    else:
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
        user_update_form = UserUpdateForm(instance=request.user)
    return render(request, 'main/settings.html', {'profile_update_form': profile_update_form, 'user_update_form': user_update_form})