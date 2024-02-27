import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_news_post_page(client):
    """
    Realiza uma requisição na paǵina de postagem de newsletters.
    """
    response = client.get(reverse('newsletter:post'))
    return response


def test_status_code_news_post_page(resp_news_post_page):
    """
    Certifica de que a página de postagem de newsletters foi carregada com sucesso.
    """
    assert resp_news_post_page.status_code == 200


def test_form_fields_news_post_page(resp_news_post_page):
    """
    Certifica de que os campos do formulário estão presentes na página.
    """
    assert_contains(resp_news_post_page, '<label for="id_title">Título:</label>')
    assert_contains(resp_news_post_page, '<input type="text" name="title" maxlength="64" required id="id_title">')
    assert_contains(resp_news_post_page, '<label for="id_intro">Introdução:</label>')
    assert_contains(resp_news_post_page, '<textarea name="intro" cols="40" rows="10" maxlength="512" '
                                         'required id="id_intro">\n</textarea>')
    assert_contains(resp_news_post_page, '<label for="id_content">Conteúdo:</label>')
    assert_contains(resp_news_post_page, '<label for="id_content">Conteúdo:</label>')
    # assert_contains(resp_news_post_page, 'testar conteúdo do container após corrigido problema do ck-editor')
    assert_contains(resp_news_post_page, '<label for="id_author">Autor:</label>')
    assert_contains(resp_news_post_page, '<input type="text" name="author" maxlength="32" required id="id_author">')
    assert_contains(resp_news_post_page, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_news_post_page, '<input type="text" name="slug" maxlength="50" required id="id_slug">')
