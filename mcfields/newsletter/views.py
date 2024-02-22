from django.shortcuts import render


def indice_newsletters(request):
    return render(request, 'newsletter/indice_newsletter.html')
