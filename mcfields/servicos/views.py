from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from mcfields.servicos.forms import ServicoForm
from mcfields.servicos.models import Servico


def detalhe_servico(request, slug):
    servico = Servico.objects.get(slug=slug)
    return render(request, 'servicos/detalhe_servico.html', {'servico': servico})


@login_required
@permission_required('servicos.add_servico', login_url='/nao_permitido/')
def adicionar_servico(request):
    if request.POST:
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            path = request.path
            return render(request, 'base/post_success.html',
                          {'titulo': request.POST['title'], 'path': path})
        else:
            return render(request, 'servicos/adicao_servico.html', {'form': form})
    form = ServicoForm()
    return render(request, 'servicos/adicao_servico.html', {'form': form})


@login_required
@permission_required('servicos.change_servico', login_url='/nao_permitido/')
def editar_servico(request, id):
    servico = Servico.objects.get(id=id)
    if request.POST:
        form = ServicoForm(request.POST, request.FILES, instance=servico)
        if form.is_valid():
            form.save()
            return render(request, 'base/edicao_concluida.html', {'servico': servico})
    form = ServicoForm(instance=servico)
    return render(request, 'servicos/adicao_servico.html', {'form': form, 'servico': servico})
