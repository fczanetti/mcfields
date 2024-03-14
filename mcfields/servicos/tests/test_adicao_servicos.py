import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.django_assertions import assert_true, assert_contains, assert_false
from mcfields.servicos.models import Service


@pytest.fixture
def service(db):
    """
    Cria um serviço e salva no banco de dados.
    """
    servico = baker.make(Service, content='Conteúdo serviço', slug='teste-slug-repetida')
    return servico


@pytest.fixture
def resp_post_serv_slug_repetida(client_usuario_log_com_perm_adic_serv, imagem):
    """
    Tenta realizar a postagem de um novo serviço com slug repetida.
    """
    resp = client_usuario_log_com_perm_adic_serv.post(reverse('servicos:adicionar'),
                                                      {'title': 'Título slug repetida',
                                                       'intro': 'Introdução slug repetida',
                                                       'home_picture': imagem,
                                                       'content': 'Conteúdo slug repetida',
                                                       'slug': 'teste-slug-repetida'})
    return resp


@pytest.fixture
def resp_adicao_novo_servico(client_usuario_log_com_perm_adic_serv, imagem):
    """
    Adiciona um novo serviço.
    """
    resp = client_usuario_log_com_perm_adic_serv.post(reverse('servicos:adicionar'),
                                                      {'title': 'Título do serviço',
                                                       'intro': 'Introdução do serviço',
                                                       'home_picture': imagem,
                                                       'content': 'Conteúdo do serviço',
                                                       'slug': 'titulo-do-servico'})
    return resp


def test_adicao_servico(resp_adicao_novo_servico):
    """
    Certifica de que o serviço foi de fato adicionado ao banco de dados.
    """
    saved_service = False
    if Service.objects.get(slug='titulo-do-servico'):
        saved_service = True
    assert_true(saved_service)


def test_msg_servico_slug_repetida(service, resp_post_serv_slug_repetida):
    """
    Certifica de que a mensagem de slug repetida é exibida para o usuário.
    """
    assert_contains(resp_post_serv_slug_repetida, 'Service com este Slug já existe.')


def test_servico_slug_repetida_nao_salvo(service, resp_post_serv_slug_repetida):
    """
    Certifica de que o serviço com slug repetida não foi salvo no banco de dados.
    """
    saved = False
    if Service.objects.filter(title='Título slug repetida'):
        saved = True
    assert_false(saved)


def test_adic_servico_concluida(resp_adicao_novo_servico):
    """
    Certifica de que, após adicionar novo serviço, a página com a mensagem de adição com sucesso é renderizada.
    """
    assert_contains(resp_adicao_novo_servico, "<title>McField's - Publicação concluída</title>")
    assert_contains(resp_adicao_novo_servico, 'O serviço "<strong>Título do serviço</strong>" '
                                              'foi adicionado com sucesso.')
