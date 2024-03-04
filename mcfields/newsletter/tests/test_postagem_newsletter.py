from unittest.mock import Mock

import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.django_assertions import assert_contains, assert_true, assert_false
from mcfields.newsletter import views
from mcfields.newsletter.models import Newsletter


@pytest.fixture
def newsletter(db):
    """
    Cria uma newsletter com slug pre-definida.
    :return:
    """
    news = baker.make(Newsletter, content='Conteúdo news slug repetida', slug='teste-slug-repetida')
    return news


@pytest.fixture
def resp_post_news_repeated_slug(client_usuario_logado_com_perm_postagem, newsletter, db):
    """
    Tenta realizar uma postagem de newsletter com slug já existente no bando de dados.
    """
    response = client_usuario_logado_com_perm_postagem.post(reverse('newsletter:post'),
                                                            {'title': 'Titulo newsletter repetida',
                                                             'intro': 'Introdução newsletter repetida',
                                                             'content': 'Conteúdo newsletter repetida',
                                                             'author': 'Autor newsletter repetida',
                                                             'slug': 'teste-slug-repetida',
                                                             'criar_rascunho': 'YES'})
    return response


@pytest.fixture
def resp_post_news_success(client_usuario_logado_com_perm_postagem, db):
    """
    Realiza a postagem de uma nova newsletter.
    """
    views.criar_rascunho = Mock()
    response = client_usuario_logado_com_perm_postagem.post(reverse('newsletter:post'),
                                                            {'title': 'Titulo teste news',
                                                             'intro': 'Introdução da newsletter',
                                                             'content': 'Conteúdo da newsletter',
                                                             'author': 'Autor da newsletter',
                                                             'slug': 'titulo-teste-news',
                                                             'criar_rascunho': 'YES'})
    return response


def test_render_page_after_post(resp_post_news_success):
    """
    Certifica de que a página de postagem com sucesso é renderizada após a postagem de uma newsletter.
    """
    assert resp_post_news_success.status_code == 200


def test_titulo_pagina_postagem_concluida(resp_post_news_success):
    """
    Certifica de que o título da página de postagem de newsletter concluída está presente e correto.
    """
    assert_contains(resp_post_news_success, "<title>McField's - Postagem concluída</title>")


def test_path_after_post_newsletter(resp_post_news_success):
    """
    Certifica de que o usuário é mantido na mesma url após a postagem da newsletter.
    """
    assert resp_post_news_success.wsgi_request.path == '/newsletter/adm/post'


def test_title_on_post_success_page(resp_post_news_success):
    """
    Certifica de que o título da newsletter está presente na página de postagem com sucesso.
    """
    assert_contains(resp_post_news_success, 'Titulo teste news')


def test_news_successfuly_saved(resp_post_news_success):
    """
    Certifica de que a newsletter foi de fato cadastrada e salva no banco de dados.
    """
    saved_news = False
    if Newsletter.objects.filter(slug='titulo-teste-news'):
        saved_news = True
    assert_true(saved_news)


def test_posted_news_in_index(client, resp_post_news_success):
    """
    Certifica de que a newsletter cadastrada está sendo exibida na página de índice de newsletter.
    """
    response = client.get(reverse('newsletter:indice_newsletters'))
    assert_contains(response, '<h4 class="newsletter-title">Titulo teste news</h4>')


def test_post_newsletter_slug_repetida(resp_post_news_repeated_slug):
    """
    Certifica de que a mensagem de erro é exibida ao tentar postar uma newsletter com slug repetida.
    """
    assert_contains(resp_post_news_repeated_slug, 'Newsletter com este Slug já existe.')


def test_news_repeated_slug_not_saved(resp_post_news_repeated_slug):
    """
    Certifica de que a newsletter com slug repetida não foi salva no banco de dados.
    """
    saved_news = False
    if Newsletter.objects.filter(title='Titulo newsletter repetida'):
        saved_news = True
    assert_false(saved_news)


def test_criacao_rascunho_sendgrid_ao_postar(client_usuario_logado_com_perm_postagem):
    """
    Certifica de que, ao postar uma newsletter, a função de
    criação de rascunhos no Sendgrid é acionada.
    """
    views.criar_rascunho = Mock()
    client_usuario_logado_com_perm_postagem.post(reverse('newsletter:post'),
                                                 {'title': 'Titulo teste news 2',
                                                  'intro': 'Introdução da newsletter 2',
                                                  'content': 'Conteúdo da newsletter 2',
                                                  'author': 'Autor da newsletter 2',
                                                  'slug': 'titulo-teste-news-2',
                                                  'criar_rascunho': 'YES'})
    views.criar_rascunho.assert_called_once()


def test_nao_criacao_rascunho_sendgrid(client_usuario_logado_com_perm_postagem):
    """
    Certifica de que o rascunho não é criado se o usuário não escolher a opção de criar.
    """
    views.criar_rascunho = Mock()
    client_usuario_logado_com_perm_postagem.post(reverse('newsletter:post'),
                                                 {'title': 'Titulo teste news 2',
                                                  'intro': 'Introdução da newsletter 2',
                                                  'content': 'Conteúdo da newsletter 2',
                                                  'author': 'Autor da newsletter 2',
                                                  'slug': 'titulo-teste-news-2',
                                                  'criar_rascunho': 'NO'})
    views.criar_rascunho.assert_not_called()
