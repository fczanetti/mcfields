from django.shortcuts import render
from mcfields.servicos.models import Servico


def detalhe_servico(request, slug):
    servico = Servico.objects.get(slug=slug)
    return render(request, 'servicos/detalhe_servico.html', {'servico': servico})
