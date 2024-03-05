from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from mcfields.servicos.forms import ServicoForm
from mcfields.servicos.models import Servico


def detalhe_servico(request, slug):
    servico = Servico.objects.get(slug=slug)
    return render(request, 'servicos/detalhe_servico.html', {'servico': servico})


@login_required
@permission_required('servicos.add_servico', login_url='/servicos/nao_permitido/')
def adicionar_servico(request):
    form = ServicoForm()
    return render(request, 'servicos/adicao_servico.html', {'form': form})