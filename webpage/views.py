from django.shortcuts import render

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def sels(request):
    return render(request, 'sels.html')

def map(request):
    return render(request, 'map.html')


# Create your views here.
