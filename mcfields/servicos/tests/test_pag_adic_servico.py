import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_adic_serv_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de adição de serviços com usuário não logado.
    """
    resp = client.get(reverse('servicos:adicionar'))
    return resp


@pytest.fixture
def resp_pag_adic_serv_usuario_logado_sem_perm(client_usuario_logado):
    """
    Realiza uma requisição na página de adição de serviços com usuário logado
    e sem permissão de adição.
    """
    resp = client_usuario_logado.get(reverse('servicos:adicionar'))
    return resp


@pytest.fixture
def resp_pag_adic_servico_usuario_logado_com_perm(client_usuario_log_com_perm_adic_serv):
    """
    Realiza uma requisição na página de adicionar serviços com usuário não logado.
    """
    resp = client_usuario_log_com_perm_adic_serv.get(reverse('servicos:adicionar'))
    return resp


def test_redirect_usuario_nao_logado(resp_pag_adic_serv_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar página de adição de serviços com usuário não logado,
    o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_adic_serv_usuario_nao_logado.status_code == 302
    assert resp_pag_adic_serv_usuario_nao_logado.url.startswith('/accounts/login/')


def test_redirect_usuario_logado_sem_perm_adicao_serv(resp_pag_adic_serv_usuario_logado_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de serviços com usuário logado e sem
    permissão de adição, o mesmo é redirecionado para a página de acesso não permitido.
    """
    assert resp_pag_adic_serv_usuario_logado_sem_perm.url.startswith('/nao_permitido/')
    assert resp_pag_adic_serv_usuario_logado_sem_perm.status_code == 302


def test_status_code_pag_adic_serv_usuario_nao_logado(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de serviços com usuário
    logado e com permissão a página carrega normalmente.
    """
    assert resp_pag_adic_servico_usuario_logado_com_perm.status_code == 200


def test_title_pag_adic_servicos(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que o título da página de adição de serviços está presente e correto.
    """
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm,
                    "<title>McField's - Novo Serviço</title>")


def test_form_adic_serv(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que os campos do formulário de adição de serviços estão presentes.
    """
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_title">Título:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<input type="text" name="title" maxlength="64" '
                                                                   'required id="id_title">')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_intro">Introdução:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<textarea name="intro" cols="40" rows="10" '
                                                                   'maxlength="512" required '
                                                                   'id="id_intro">\n</textarea>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_home_picture">Foto da home '
                                                                   'page:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<input type="file" name="home_picture" '
                                                                   'accept="image/*" required id="id_home_picture">')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_content">Conteúdo:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<div class="ck-editor-container">')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<input type="text" name="slug" maxlength="64" '
                                                                   'required id="id_slug">')


def test_direcionamento_botao_cancelar(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que o botão cancelar, no momento da adição de um novo serviço, tem a função
    de direcionar o usuário para a home page.
    """
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, f'<a class="canc-button" '
                                                                   f'href="{reverse("base:home")}">Cancelar</a>')


def test_titulo_form(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que o título do formulário está presente e
    indicando a adição de um novo serviço.
    """
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<h1 class="form-title">Novo Serviço</h1>')
