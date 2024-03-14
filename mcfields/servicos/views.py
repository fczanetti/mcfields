from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render

from mcfields.servicos.forms import ServiceForm
from mcfields.servicos.models import Service


def detalhe_servico(request, slug):
    service = Service.objects.get(slug=slug)
    return render(request, 'servicos/detalhe_servico.html', {'servico': service})


@login_required
@permission_required('servicos.add_service', login_url='/nao_permitido/')
def adicionar_servico(request):
    if request.POST:
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            path = request.path
            return render(request, 'base/post_success.html',
                          {'titulo': request.POST['title'], 'path': path})
        else:
            return render(request, 'servicos/adicao_servico.html', {'form': form})
    form = ServiceForm()
    return render(request, 'servicos/adicao_servico.html', {'form': form})


@login_required
@permission_required('servicos.change_service', login_url='/nao_permitido/')
def editar_servico(request, id):
    service = Service.objects.get(id=id)
    if request.POST:
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return render(request, 'base/edicao_concluida.html', {'servico': service})
    form = ServiceForm(instance=service)
    return render(request, 'servicos/adicao_servico.html', {'form': form, 'servico': service})


@login_required
@permission_required('servicos.delete_service', login_url='/nao_permitido/')
def remocao_servico(request, id):
    service = Service.objects.get(id=id)
    if request.method == 'POST':
        titulo = service.title
        path = request.path
        service.delete()
        return render(request, 'base/remocao_concluida.html', {'titulo': titulo, 'path': path})
    return render(request, 'servicos/confirmacao_remocao.html', {'servico': service})
