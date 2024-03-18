import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_edicao_usuario_nao_logado(client, newsletter):
    """
    Realiza uma requisição na página de edição de newsletter com usuário não logado.
    """
    response = client.get(reverse('newsletter:edicao', args=(newsletter.id,)))
    return response


@pytest.fixture
def resp_pag_edicao_usuario_logado_sem_perm(client_usuario_logado, newsletter):
    """
    Realiza uma requisição na página de edição de newsletter com usuário logado e sem permissão de edição.
    """
    response = client_usuario_logado.get(reverse('newsletter:edicao', args=(newsletter.id,)))
    return response


@pytest.fixture
def resp_pag_edicao_usuario_logado_com_perm(client_usuario_logado_com_perm_edicao, newsletter):
    """
    Realiza uma requisição na página de edição de newsletter com usuário logado e com permissão de edição.
    """
    response = client_usuario_logado_com_perm_edicao.get(reverse('newsletter:edicao', args=(newsletter.id,)))
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
    assert resp_pag_edicao_usuario_logado_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_edicao_newsletter(resp_pag_edicao_usuario_logado_com_perm):
    """
    Certifica de que ao tentar acessar a página de edição de newsletter com usuário logado e permissão concedida
    esta é carregada corretamente, além de ter os componentes do formulário exibidos.
    """
    assert resp_pag_edicao_usuario_logado_com_perm.status_code == 200
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_title">Título:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_intro">Introdução:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_content">Conteúdo:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_author">Autor:</label>')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, '<label for="id_slug">Slug:</label>')


def test_titulo_pag_edicao_newsletter(resp_pag_edicao_usuario_logado_com_perm):
    """
    Certifica de que o título da página de edição de newsletter está presente e correto.
    """
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, "<title>McField's - Edição de Newsletter</title>")


def test_infos_newsletter_pag_edicao(newsletter, resp_pag_edicao_usuario_logado_com_perm):
    """
    Certifica de que o conteúdo da newsletter está presente na página de edição.
    :return:
    """
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, f'<input type="text" name="title" '
                                                             f'value="{newsletter.title}" maxlength="64" '
                                                             f'required id="id_title">')
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, newsletter.intro)
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, newsletter.content)
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, newsletter.author)
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, newsletter.slug)


def test_botao_cancelar_edicao(resp_pag_edicao_usuario_logado_com_perm):
    """
    Certifica de que o botão de cancelamento de edição está presente na página de edição de newsletter.
    """
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, f'<a class="canc-button" '
                                                             f'href="{reverse("newsletter:indice_newsletters")}">'
                                                             f'Cancelar</a>')


def test_titulo_form(resp_pag_edicao_usuario_logado_com_perm, newsletter):
    """
    Certifica de que o título do formulário está presente e indicando
    a edição de uma newsletter existente.
    """
    assert_contains(resp_pag_edicao_usuario_logado_com_perm, f'<h1 class="form-title">Edição da Newsletter '
                                                             f'"{newsletter.title}"</h1>')
