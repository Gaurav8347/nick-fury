from django.shortcuts import render, redirect
from .models import customer_dictionary
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def welcome(request):
    return render(request, 'welcome.html')



