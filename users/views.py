from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .forms import UserRegisterForm

def login(request):
    return render(request, 'users/login.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Account created successfully. You can now login using these credentials.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})