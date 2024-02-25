from django.shortcuts import render

from mcfields.newsletter.models import Newsletter


def indice_newsletters(request):
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter/indice_newsletter.html', {'newsletters': newsletters})


def detalhe_newsletter(request, slug):
    newsletter = Newsletter.objects.get(slug=slug)
    return render(request, 'newsletter/detalhe_newsletter.html', {'newsletter': newsletter})
