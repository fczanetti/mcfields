from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from mcfields import settings
from mcfields.base.forms import EmailForm
from sendgrid import SendGridAPIClient
from mcfields.servicos.models import Servico


def home(request):
    servicos = Servico.objects.all()
    return render(request, 'base/home.html', {'servicos': servicos})


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
                list_id=settings.SENDGRID_NEWSLETTER_LIST_ID
            )
            return render(request, 'base/inscricao_concluida.html', {'email': email})
    return redirect(reverse('base:home'))


def cadastrar_email(key, user_email, list_id):
    sg = SendGridAPIClient(key)
    data = {"contacts": [{"email": user_email}], 'list_ids': [list_id]}
    return sg.client.marketing.contacts.put(request_body=data)


class UserLogin(LoginView):
    template_name = 'registration/user_login.html'
    next_page = '/'
