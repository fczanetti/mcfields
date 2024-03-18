import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_news_post_page(client):
    """
    Realiza uma requisição na paǵina de postagem de newsletters sem usuário logado.
    """
    response = client.get(reverse('newsletter:post'))
    return response


@pytest.fixture
def resp_news_post_page_usuario_logado(client_usuario_logado):
    """
    Realiza uma requisição na página de postagem de newsletter com usuário logado sem permissão.
    """
    response = client_usuario_logado.get(reverse('newsletter:post'))
    return response


@pytest.fixture
def resp_post_page_usuario_logado_com_permissao(client_usuario_logado_com_perm_postagem):
    """
    Realiza uma requisição na página de postagem de newsletter com usuário logado e permissão concedida.
    """
    response = client_usuario_logado_com_perm_postagem.get(reverse('newsletter:post'))
    return response


def test_redirect_news_post_page(resp_news_post_page):
    """
    Certifica de que a página de postagem de newsletters não foi carregada e o usuário foi redirecionado
    para a página de login.
    """
    assert resp_news_post_page.status_code == 302
    assert resp_news_post_page.url.startswith('/accounts/login/')


def test_redirect_usuario_logado_sem_permissao(resp_news_post_page_usuario_logado):
    """
    Certifica de que o usuário logado e sem permissão seja redirecionado para a página de acesso não permitido
    ao tentar acessar a página de postagem de newsletter.
    """
    assert resp_news_post_page_usuario_logado.status_code == 302
    assert resp_news_post_page_usuario_logado.url.startswith('/nao_permitido')


def test_form_fields_news_post_page(resp_post_page_usuario_logado_com_permissao):
    """
    Certifica de que o usuário logado e com permissão de postagem consegue acessar a página de postagem e os campos do
    formulário estão presentes.
    """
    assert resp_post_page_usuario_logado_com_permissao.status_code == 200
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<label for="id_title">Título:</label>')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<input type="text" name="title" maxlength="64" '
                                                                 'required id="id_title">')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<label for="id_intro">Introdução:</label>')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<textarea name="intro" cols="40" rows="10" '
                                                                 'maxlength="512" required id="id_intro">\n</textarea>')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<label for="id_content">Conteúdo:</label>')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<div class="ck-editor-container">')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<label for="id_author">Autor:</label>')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<input type="text" name="author" maxlength="32" '
                                                                 'required id="id_author">')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<input type="text" name="slug" maxlength="50" '
                                                                 'required id="id_slug">')


def test_titulo_pag_postagem_newsletter(resp_post_page_usuario_logado_com_permissao):
    """
    Certifica de que o título da página de postagem de newsletter está presente e correto.
    """
    assert_contains(resp_post_page_usuario_logado_com_permissao, "<title>McField's - Nova Newsletter</title>")


def test_botao_canc_postagem(resp_post_page_usuario_logado_com_permissao):
    """
    Certifica de que o botão de cancelar postagem está presente na página de postagem de newsletter.
    """
    assert_contains(resp_post_page_usuario_logado_com_permissao, f'<a class="canc-button" '
                                                                 f'href="{reverse("newsletter:indice_newsletters")}">'
                                                                 f'Cancelar</a>')


def test_titulo_form(resp_post_page_usuario_logado_com_permissao):
    """
    Certifica de que o título do formulário está presente
    e indicando adição de uma nova newsletter.
    """
    assert_contains(resp_post_page_usuario_logado_com_permissao, '<h1 class="form-title">Nova Newsletter</h1>')
