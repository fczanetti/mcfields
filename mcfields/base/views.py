from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from mcfields import settings
from mcfields.base.forms import EmailForm, SubjectForm
from mcfields.base import facade
from mcfields.base.models import Subject
from mcfields.servicos.models import Service


def home(request):
    services = Service.objects.all()
    return render(request, 'base/home.html', {'servicos': services})


def sobre(request):
    return render(request, 'base/sobre.html')


def inscricao_email(request):
    """
    Antes de inscrever um email é verificado se este está registrado no grupo de emails descadastrados.
    Caso esteja, o email será apenas removido do grupo e passará a receber emails novamente. Caso esteja
    no grupo de descadastrados não é necessário adicioná-lo à lista de emails, pois este já estará presente.
    :param request:
    :return:
    """
    if request.POST:
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            email = emailform.cleaned_data['email']
            api_key = settings.SENDGRID_API_KEY
            sg_list_id = settings.SENDGRID_LIST_ID
            suppr_group_id = settings.SUPPRESSION_GROUP_ID
            resp_email_desc = facade.checar_email_descadastrado(key=api_key, email=email, suppr_group_id=suppr_group_id)
            if bytes(email, 'utf-8') in resp_email_desc.body:
                facade.remover_da_lista_desc(key=api_key, email=email, supp_group_id=suppr_group_id)
            else:
                facade.cadastrar_email(key=api_key, user_email=email, list_id=sg_list_id)
            return render(request, 'base/inscricao_concluida.html', {'email': email})
    return redirect(reverse('base:home'))


@login_required
def nao_permitido(request):
    return render(request, 'base/nao_permitido.html')


class UserLogin(LoginView):
    template_name = 'registration/user_login.html'
    next_page = '/'


@login_required
@permission_required('base.add_subject', login_url='/nao_permitido/')
def adic_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            titulo = request.POST['title']
            path = request.path
            return render(request, 'base/post_success.html', {'titulo': titulo, 'path': path})
        else:
            return render(request, 'base/adic_subject.html', {'form': form})
    form = SubjectForm()
    return render(request, 'base/adic_subject.html', {'form': form})


@login_required
@permission_required('base.change_subject', login_url='/nao_permitido/')
def edic_subject(request, id):
    subject = Subject.objects.get(id=id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return render(request, 'base/edicao_concluida.html', {'subject': subject})
        else:
            return render(request, 'base/adic_subject.html', {'form': form, 'subject': subject})
    form = SubjectForm(instance=subject)
    return render(request, 'base/adic_subject.html', {'form': form, 'subject': subject})


@login_required
@permission_required('base.view_subject', login_url='/nao_permitido/')
def subjects(request):
    subs = facade.buscar_subjects_com_conteudos()
    return render(request, 'base/assuntos.html', {'subjects': subs})


@login_required
@permission_required('base.delete_subject', login_url='/nao_permitido/')
def remoc_subject(request, id):
    """
    Acessa a página de remoção e remove assuntos. A página de remoção só será acessada se o assunto a ser
    removido não possuir nenhum outro conteúdo relacionado, caso contrário o usuário será direcionado para
    a página de remoção não permitida.
    """
    sub = Subject.objects.get(id=id)
    titulo = sub.title
    if sub.video_set.exists() or sub.newsletter_set.exists():
        return render(request, 'base/remocao_nao_permitida.html', {'titulo': titulo})
    if request.method == 'POST':
        path = request.path
        sub.delete()
        return render(request, 'base/remocao_concluida.html', {'titulo': titulo, 'path': path})
    return render(request, 'base/conf_remoc_subject.html', {'subject': sub})


def politica_privac(request):
    return render(request, 'base/politica_privacidade.html')
