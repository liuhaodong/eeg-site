from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def mainpage(request):
    return render(request, 'homepage.html')
