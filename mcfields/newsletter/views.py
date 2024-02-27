from django.shortcuts import render
# from django.urls import reverse

from mcfields.newsletter.forms import NewsletterForm
from mcfields.newsletter.models import Newsletter


def indice_newsletters(request):
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter/indice_newsletter.html', {'newsletters': newsletters})


def detalhe_newsletter(request, slug):
    newsletter = Newsletter.objects.get(slug=slug)
    return render(request, 'newsletter/detalhe_newsletter.html', {'newsletter': newsletter})


def post_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'newsletter/post_newsletter_success.html',
                          {'titulo': request.POST['title']})
        else:
            return render(request, 'newsletter/post_newsletter.html', {'form': form})
    form = NewsletterForm()
    return render(request, 'newsletter/post_newsletter.html', {'form': form})
