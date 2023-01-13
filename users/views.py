from django.shortcuts import render
from django.contrib import auth

def login(request):
    return render(request, r'users\login')