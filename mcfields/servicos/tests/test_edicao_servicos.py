import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.django_assertions import assert_contains
from mcfields.servicos.models import Service


@pytest.fixture
def resp_edicao_servico(service, imagem, client_usuario_log_com_perm_edic_serv):
    """
    Realiza uma alteração em um serviço existente.
    """
    resp = client_usuario_log_com_perm_edic_serv.post(reverse('servicos:edicao', args=(service.pk,)),
                                                      {'title': 'Título alterado',
                                                       'intro': 'Introdução alterada',
                                                       'home_picture': imagem,
                                                       'content': 'Conteúdo alterado',
                                                       'slug': 'titulo-alterado'})
    return resp


def test_redirect_edicao_servico(resp_edicao_servico, service):
    """
    Certifica de que, após a edição feita, o usuário é
    direcionado para a página de edição concluída.
    """
    assert resp_edicao_servico.status_code == 200
    assert resp_edicao_servico.wsgi_request.path == f'/servicos/adm/edicao/{service.pk}'


def test_pag_edicao_servico_sucesso(resp_edicao_servico):
    """
    Certifica de que a página de edição concluída possui a mensagem
    informando a edição bem sucedida. O título do serviço deve estar
    presente na mensagem.
    """
    assert_contains(resp_edicao_servico, 'O serviço "<strong>Título alterado</strong>" foi editado com sucesso.')


def test_alteracoes_servico_editado(resp_edicao_servico, service):
    """
    Certifica de que a alteração feita foi salva no banco de dados.
    """
    serv = Service.objects.get(id=service.pk)
    assert serv.title == 'Título alterado'
    assert serv.intro == 'Introdução alterada'
    assert serv.content == 'Conteúdo alterado'


def test_tentativa_edicao_slug_repetida(service, imagem, client_usuario_log_com_perm_edic_serv):
    """
    Certifica de que, ao tentar editar um serviço inserindo uma slug já existente no banco de dados,
    a mensagem de erro é exibida para o usuário.
    """
    baker.make(Service, content='Conteúdo', slug='slug-repetida')
    resp = client_usuario_log_com_perm_edic_serv.post(reverse('servicos:edicao', args=(service.pk,)),
                                                      {'title': service.title,
                                                       'intro': service.intro,
                                                       'home_picture': imagem,
                                                       'content': service.content,
                                                       'slug': 'slug-repetida'})
    assert_contains(resp, 'Service com este Slug já existe.')
