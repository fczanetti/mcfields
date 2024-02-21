from django.shortcuts import render


def home(request):
    return render(request, 'base/home.html')


def sobre(request):
    return render(request, 'base/sobre.html')
