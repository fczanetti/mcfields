from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from mcfields import settings
from mcfields.newsletter import facade
from mcfields.newsletter.forms import NewsletterForm
from mcfields.newsletter.models import Newsletter


def indice_newsletters(request):
    newsletters = facade.listar_newsletters_ordenadas()
    return render(request, 'newsletter/indice_newsletter.html', {'newsletters': newsletters})


def detalhe_newsletter(request, slug, subject_slug):
    newsletter = Newsletter.objects.select_related('subject').get(slug=slug)
    return render(request, 'newsletter/detalhe_newsletter.html', {'newsletter': newsletter})


@login_required
@permission_required('newsletter.add_newsletter', login_url='/nao_permitido/')
def post_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            path = request.path
            api_key = settings.SENDGRID_API_KEY
            titulo = request.POST['title']
            sg_list_id = settings.SENDGRID_LIST_ID
            sg_news_design_id = settings.SENDGRID_NEWSLETTER_DESIGN_ID
            if request.POST['criar_rascunho'] == 'YES':
                facade.criar_rascunho(key=api_key, titulo=titulo, list_id=sg_list_id, design_id=sg_news_design_id)
            return render(request, 'base/post_success.html',
                          {'titulo': request.POST['title'], 'path': path})
        else:
            return render(request, 'newsletter/post_newsletter.html', {'form': form})
    form = NewsletterForm()
    return render(request, 'newsletter/post_newsletter.html', {'form': form})


@login_required
@permission_required('newsletter.change_newsletter', login_url='/nao_permitido/')
def edicao_newsletter(request, id):
    newsletter = Newsletter.objects.get(id=id)
    if request.POST:
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            api_key = settings.SENDGRID_API_KEY
            titulo = request.POST['title']
            sg_list_id = settings.SENDGRID_LIST_ID
            sg_news_design_id = settings.SENDGRID_NEWSLETTER_DESIGN_ID
            if request.POST['criar_rascunho'] == 'YES':
                facade.criar_rascunho(key=api_key, titulo=titulo, list_id=sg_list_id, design_id=sg_news_design_id)
            return render(request, 'base/edicao_concluida.html',
                          {'newsletter': newsletter})
        else:
            return render(request, 'newsletter/post_newsletter.html',
                          {'form': form, 'newsletter': newsletter})
    form = NewsletterForm(instance=newsletter)
    return render(request, 'newsletter/post_newsletter.html',
                  {'form': form, 'newsletter': newsletter})


@login_required
@permission_required('newsletter.delete_newsletter', login_url='/nao_permitido/')
def remocao_newsletter(request, id):
    newsletter = Newsletter.objects.get(id=id)
    if request.method == 'POST':
        titulo = newsletter.title
        newsletter.delete()
        path = request.path
        return render(request, 'base/remocao_concluida.html', {'titulo': titulo, 'path': path})
    return render(request, 'newsletter/confirmacao_remocao.html', {'newsletter': newsletter})
