from django.shortcuts import render, redirect
from users.forms import ProfileUpdateForm
from users.models import Profile
from django.contrib import messages


def index(request):
    return render(request, 'main/index.html')


def settings_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.Profile)
        if form.is_valid:
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('settings')
    else:
        form = ProfileUpdateForm()
    return render(request, 'main/settings.html', {'profile_edit_form': form})