import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_rem_news_usuario_nao_logado(client, newsletter):
    """
    Realiza uma requisição na página de remoção de newsletter com usuário não logado.
    """
    resp = client.get(reverse('newsletter:remocao', args=(newsletter.id,)))
    return resp


@pytest.fixture
def resp_pag_rem_news_usuario_logado_sem_perm(client_usuario_logado, newsletter):
    """
    Realiza uma requisição na página de remoção de newsletter com
    usuário logado porém sem permissão de remoção.
    """
    resp = client_usuario_logado.get(reverse('newsletter:remocao', args=(newsletter.id,)))
    return resp


@pytest.fixture
def resp_pag_rem_news_usuario_logado_com_perm(client_usuario_logado_com_perm_remocao, newsletter):
    """
    Realiza uma requisição na página de remoção de newsletter
    com usuário logado e com permissão de remoção.
    """
    resp = client_usuario_logado_com_perm_remocao.get(reverse('newsletter:remocao', args=(newsletter.id,)))
    return resp


def test_redirect_usuario_nao_logado(resp_pag_rem_news_usuario_nao_logado):
    """
    Certifica de que o usuário não logado, ao tentar acessar a página de remoção de newsletter,
    é redirecionado para a página de login.
    """
    assert resp_pag_rem_news_usuario_nao_logado.status_code == 302
    assert resp_pag_rem_news_usuario_nao_logado.url.startswith('/accounts/login/')


def test_redirect_usuario_logado_sem_perm_remocao(resp_pag_rem_news_usuario_logado_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de remoção de newsletter com usuário
    logado sem permissão, o mesmo é redirecionado para a página de acesso não permitido.
    """
    assert resp_pag_rem_news_usuario_logado_sem_perm.status_code == 302
    assert resp_pag_rem_news_usuario_logado_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_remocao_newsletter(resp_pag_rem_news_usuario_logado_com_perm):
    """
    Certifica de que, ao tentar acessar a página de remoção de newsletter com usuário
    logado e com permissão, a página é carregada com sucesso.
    """
    assert resp_pag_rem_news_usuario_logado_com_perm.status_code == 200


def test_titulo_pagina_remocao(resp_pag_rem_news_usuario_logado_com_perm):
    """
    Certifica de que o título da página de confirmação de remoção de
    newsletter está presente e correto.
    """
    assert_contains(resp_pag_rem_news_usuario_logado_com_perm, "<title>McField's - Confirmar remoção</title>")


def test_titulo_news_pag_remocao(resp_pag_rem_news_usuario_logado_com_perm, newsletter):
    """
    Certifica de que o título da newsletter a ser removida está presente na página de
    confirmação de remoção.
    """
    assert_contains(resp_pag_rem_news_usuario_logado_com_perm, newsletter.title)


def test_botoes_pag_remocao(resp_pag_rem_news_usuario_logado_com_perm, newsletter):
    """
    Certifica de que os botões do formulário de remoção de newsletter
    estão presentes na página de confirmação de remoção.
    """
    assert_contains(resp_pag_rem_news_usuario_logado_com_perm,
                    f'<a id="canc-removal-button" '
                    f'href="{reverse("newsletter:detalhe_newsletter", args=(newsletter.slug,))}">'
                    f'Cancelar</a>')
    assert_contains(resp_pag_rem_news_usuario_logado_com_perm, '<button id="conf-removal-button" type="submit">'
                                                               'Confirmar</button>')
