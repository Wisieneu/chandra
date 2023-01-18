from django.shortcuts import render
from users.forms import ProfileUpdateForm



def index(request):
    return render(request, 'main/index.html')


def settings_view(request):
    form = ProfileUpdateForm()
    return render(request, 'main/settings.html', {'profile_edit_form': form})