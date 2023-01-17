from django.shortcuts import render



def index(request):
    return render(request, 'main/index.html')


def settings_view(request):
    return render(request, 'main/settings.html')