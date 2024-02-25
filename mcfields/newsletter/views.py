from django.shortcuts import render

from mcfields.newsletter.models import Newsletter


def indice_newsletters(request):
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter/indice_newsletter.html', {'newsletters': newsletters})
