from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from mcfields import settings
from mcfields.base.forms import EmailForm, SubjectForm
from sendgrid import SendGridAPIClient
from mcfields.servicos.models import Service


def home(request):
    services = Service.objects.all()
    return render(request, 'base/home.html', {'servicos': services})


def sobre(request):
    return render(request, 'base/sobre.html')


def inscricao_email(request):
    if request.POST:
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            email = emailform.cleaned_data['email']
            cadastrar_email(
                key=settings.SENDGRID_API_KEY,
                user_email=email,
                list_id=settings.SENDGRID_LIST_ID
            )
            return render(request, 'base/inscricao_concluida.html', {'email': email})
    return redirect(reverse('base:home'))


def cadastrar_email(key, user_email, list_id):
    sg = SendGridAPIClient(key)
    data = {"contacts": [{"email": user_email}], 'list_ids': [list_id]}
    return sg.client.marketing.contacts.put(request_body=data)


@login_required
def nao_permitido(request):
    return render(request, 'base/nao_permitido.html')


class UserLogin(LoginView):
    template_name = 'registration/user_login.html'
    next_page = '/'


@login_required
@permission_required('base.add_subject', login_url='/nao_permitido/')
def adic_subject(request):
    form = SubjectForm()
    return render(request, 'base/adic_subject.html', {'form': form})
