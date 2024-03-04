import pytest
from django.urls import reverse
from datetime import date
from mcfields.django_assertions import assert_contains, assert_not_contains


@pytest.fixture
def resp_detalhe_newsletter(client, newsletter):
    """
    Cria uma requisição na página de detalhes da newsletter.
    """
    response = client.get(reverse('newsletter:detalhe_newsletter', args=(newsletter.slug,)))
    return response


@pytest.fixture
def resp_detalhe_news_usuario_log_sem_perm_edicao(client_usuario_logado, newsletter):
    """
    Cria uma requisição na página de detalhes da newsletter com um usuário logado sem permissão de edição.
    """
    resp = client_usuario_logado.get(reverse('newsletter:detalhe_newsletter', args=(newsletter.slug,)))
    return resp


@pytest.fixture
def resp_detalhe_news_usuario_log_com_perm_edicao(client_usuario_logado_com_perm_edicao, newsletter):
    """
    Cria uma requisição na página de detalhes da newsletter com usuário logado e com permissão de edição.
    """
    resp = client_usuario_logado_com_perm_edicao.get(
        reverse('newsletter:detalhe_newsletter', args=(newsletter.slug,)))
    return resp


@pytest.fixture
def resp_detalhe_news_usuario_log_sem_perm_remocao(client_usuario_logado, newsletter):
    """
    Realiza uma requisição na página de detalhe da newsletter com usuário logado
    sem permissão de remoção.
    """
    resp = client_usuario_logado.get(reverse('newsletter:detalhe_newsletter', args=(newsletter.slug,)))
    return resp


@pytest.fixture
def resp_detalhe_news_usuario_log_com_perm_remocao(client_usuario_logado_com_perm_remocao, newsletter):
    """
    Realiza uma requisição na página de detalhe da newsletter com usuário logado
    sem permissão de remoção.
    """
    resp = client_usuario_logado_com_perm_remocao.get(
        reverse('newsletter:detalhe_newsletter', args=(newsletter.slug,)))
    return resp


def test_status_code_detalhe_newsletter(resp_detalhe_newsletter):
    """
    Certifica de que a página de detalhes da newsletter foi carregada com sucesso.
    """
    assert resp_detalhe_newsletter.status_code == 200


def test_titulo_pagina_detalhe_newsletter(resp_detalhe_newsletter, newsletter):
    """
    Certifica de que o título da página de detalhes da newsletter está presente e correto.
    """
    assert_contains(resp_detalhe_newsletter, f"<title>McField's - {newsletter.title}</title>")


def test_newsletter_dados(resp_detalhe_newsletter, newsletter):
    """
    Certifica de que os dados da newsletter estão presentes na página de detalhe desta.
    """
    pub_date = date.strftime(newsletter.pub_date, '%d/%m/%Y')
    assert_contains(resp_detalhe_newsletter, f'<h1 id="newsletter-title">{newsletter.title}</h1>')
    assert_contains(resp_detalhe_newsletter, newsletter.intro)
    assert_contains(resp_detalhe_newsletter, newsletter.content)
    assert_contains(resp_detalhe_newsletter, f'<div id="news-pub-date">{pub_date}</div>')
    assert_contains(resp_detalhe_newsletter, f'<div id="newsletter-author">{newsletter.author}</div>')


def test_link_edicao_usuario_nao_logado(resp_detalhe_newsletter, newsletter):
    """
    Certifica de que o link para edição da newsletter não está
    presente na página de detalhes para usuários não logados.
    """
    assert_not_contains(resp_detalhe_newsletter,
                        f'<a id="news-update-link" '
                        f'href="{reverse("newsletter:edicao", args=(newsletter.id,))}">Editar</a>')


def test_link_edicao_usuario_logado_sem_perm_edicao(resp_detalhe_news_usuario_log_sem_perm_edicao, newsletter):
    """
    Certifica de que, com um usuário logado mas sem permissão de edição,
    o link não estará presente na página de detalhes da newsletter.
    """
    assert_not_contains(resp_detalhe_news_usuario_log_sem_perm_edicao,
                        f'<a id="news-update-link" '
                        f'href="{reverse("newsletter:edicao", args=(newsletter.id,))}">Editar</a>')


def test_link_edicao_usuario_logado_com_perm_edicao(resp_detalhe_news_usuario_log_com_perm_edicao, newsletter):
    """
    Certifica de que o link de edição de newsletter aparece na página de detalhes desta para um usuário logado
    e com permissão de edição.
    """
    assert_contains(resp_detalhe_news_usuario_log_com_perm_edicao,
                    f'<a id="news-update-link" '
                    f'href="{reverse("newsletter:edicao", args=(newsletter.id,))}">Editar</a>')


def test_botao_remocao_usuario_nao_logado(resp_detalhe_newsletter, newsletter):
    """
    Certifica de que o botão de remoção de newsletter não está disponível para usuários não logados.
    """
    assert_not_contains(resp_detalhe_newsletter,
                        f'<a id="news-removal-link" href="{newsletter.get_removal_url()}">Remover</a>')


def test_botao_remocao_usuario_logado_sem_perm(resp_detalhe_news_usuario_log_sem_perm_remocao, newsletter):
    """
    Certifica de que o botão de remoção de newsletter não está
    disponível para usuários logados sem permissão de remoção.
    """
    assert_not_contains(resp_detalhe_news_usuario_log_sem_perm_remocao,
                        f'<a id="news-removal-link" href="{newsletter.get_removal_url()}">Remover</a>')


def test_botao_remocao_usuario_logado_com_perm(resp_detalhe_news_usuario_log_com_perm_remocao, newsletter):
    """
    Certifica de que o botão de remoção de newsletter não está
    disponível para usuários logados sem permissão de remoção.
    """
    assert_contains(resp_detalhe_news_usuario_log_com_perm_remocao,
                    f'<a id="news-removal-link" href="{newsletter.get_removal_url()}">Remover</a>')
