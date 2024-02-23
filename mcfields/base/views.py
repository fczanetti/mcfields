from django.shortcuts import render, redirect
from django.urls import reverse

from mcfields import settings
from mcfields.base.forms import EmailForm
from sendgrid import SendGridAPIClient


def home(request):
    if request.POST:
        emailform = EmailForm(request.POST)
        if emailform.is_valid():
            email = emailform.cleaned_data['email']
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            data = {"contacts": [{"email": email}], 'list_ids': [settings.SENDGRID_NEWSLETTER_LIST_ID]}
            response = sg.client.marketing.contacts.put(request_body=data)
            return redirect(reverse('base:inscricao_concluida'))
    return render(request, 'base/home.html')


def sobre(request):
    return render(request, 'base/sobre.html')


def inscricao_concluida(request):
    return render(request, 'base/inscricao_concluida.html')
