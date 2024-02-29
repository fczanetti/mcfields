import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_edicao_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de edição de newsletter com usuário não logado.
    """
    response = client.get(reverse('newsletter:edicao'))
    return response


@pytest.fixture
def resp_pag_edicao_usuario_logado_sem_perm(client_usuario_logado):
    """
    Realiza uma requisição na página de edição de newsletter com usuário logado e sem permissão de edição.
    """
    response = client_usuario_logado.get(reverse('newsletter:edicao'))
    return response


@pytest.fixture
def resp_pag_edicao_usuario_logado_com_perm(client_usuario_logado_com_perm_edicao):
    """
    Realiza uma requisição na página de edição de newsletter com usuário logado e com permissão de edição.
    """
    response = client_usuario_logado_com_perm_edicao.get(reverse('newsletter:edicao'))
    return response


def test_redirect_pag_edicao_usuario_nao_logado(resp_pag_edicao_usuario_nao_logado):
    """
    Certifica que, ao tentar acessar a página de edição com usuário não logado, este é redirecionado para a página
    de login.
    """
    assert resp_pag_edicao_usuario_nao_logado.status_code == 302
    assert resp_pag_edicao_usuario_nao_logado.url.startswith('/accounts/login/')


def test_redirect_pag_edicao_usuario_sem_permissao(resp_pag_edicao_usuario_logado_sem_perm):
    """
    Certifica de que ao tentar acessar a página de edição de newsletter com o usuário logado sem permissão de edição
    o mesmo é redirecionado para a página de acesso não permitido.
    """
    assert resp_pag_edicao_usuario_logado_sem_perm.status_code == 302
    assert resp_pag_edicao_usuario_logado_sem_perm.url.startswith('/newsletter/nao_permitido/')


def test_status_code_pag_edicao_newsletter(resp_pag_edicao_usuario_logado_com_perm):
    """
    Certifica de que ao tentar acessar a página de edição de newsletter com usuário logado e permissão concedida
    esta é carregada corretamente, além de ter os componentes do formulário exibidos.
    """
    assert resp_pag_edicao_usuario_logado_com_perm.status_code == 200
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_title">Título:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<input type="text" name="title" maxlength="64" '
                                                             'required id="id_title">')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_intro">Introdução:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<textarea name="intro" cols="40" rows="10" '
                                                             'maxlength="512" required id="id_intro">\n</textarea>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_content">Conteúdo:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<div class="ck-editor-container">')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_author">Autor:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<input type="text" name="author" maxlength="32" '
                                                             'required id="id_author">')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<input type="text" name="slug" maxlength="50" '
                                                             'required id="id_slug">')
