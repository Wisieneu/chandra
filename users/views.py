from django.shortcuts import render
from django.contrib import auth

def login(request):
    return render(request, 'users/login.html')

def signup(request):
    return render(request, 'users/signup.html')