from django.shortcuts import render, redirect
from django.urls import reverse

from mcfields import settings
from mcfields.base.forms import EmailForm
from sendgrid import SendGridAPIClient


def home(request):
    return render(request, 'base/home.html')


def sobre(request):
    return render(request, 'base/sobre.html')


def inscricao_email(request):
    if request.POST:
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            email = emailform.cleaned_data['email']
            if not email == 'teste@teste.com':
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                data = {"contacts": [{"email": email}], 'list_ids': [settings.SENDGRID_NEWSLETTER_LIST_ID]}
                sg.client.marketing.contacts.put(request_body=data)
            return render(request, 'base/inscricao_concluida.html', {'email': email})
    return redirect(reverse('base:home'))
