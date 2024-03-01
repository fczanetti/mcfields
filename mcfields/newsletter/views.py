from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from mcfields.newsletter.forms import NewsletterForm
from mcfields.newsletter.models import Newsletter


def indice_newsletters(request):
    newsletters = Newsletter.objects.all()
    return render(request, 'newsletter/indice_newsletter.html', {'newsletters': newsletters})


def detalhe_newsletter(request, slug):
    newsletter = Newsletter.objects.get(slug=slug)
    return render(request, 'newsletter/detalhe_newsletter.html', {'newsletter': newsletter})


@login_required
@permission_required('newsletter.add_newsletter', login_url='/newsletter/nao_permitido/')
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


@login_required
def nao_permitido(request):
    return render(request, 'newsletter/nao_permitido_newsletter.html')


@login_required
@permission_required('newsletter.change_newsletter', login_url='/newsletter/nao_permitido/')
def edicao_newsletter(request, id):
    newsletter = Newsletter.objects.get(id=id)
    if request.POST:
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            return render(request, 'newsletter/newsletter_editada.html',
                          {'titulo': request.POST['title']})
    form = NewsletterForm(instance=newsletter)
    return render(request, 'newsletter/post_newsletter.html',
                  {'form': form, 'newsletter': newsletter})
