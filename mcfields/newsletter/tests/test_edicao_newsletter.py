from unittest.mock import Mock

import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.django_assertions import assert_contains
from mcfields.newsletter import facade
from mcfields.newsletter.models import Newsletter


@pytest.fixture
def resp_alteracao_newsletter(newsletter,
                              client_usuario_logado_com_perm_edicao, subject):
    """
    Realiza a alteração em uma newsletter e retorna a resposta dessa alteração.
    """
    resp = client_usuario_logado_com_perm_edicao.post(
        reverse('newsletter:edicao', args=(newsletter.id,)),
        {'title': newsletter.title,
         'intro': 'Introdução alterada',
         'content': 'Conteúdo alterado',
         'subject': subject.pk,
         'author': newsletter.author,
         'slug': newsletter.slug,
         'criar_rascunho': 'NO'})
    return resp


def test_titulo_pag_edicao_concluida(resp_alteracao_newsletter):
    """
    Certifica de que o título da página de edição concluída está correto e presente.
    """
    assert_contains(resp_alteracao_newsletter, "<title>McField's - Edição concluída</title>")


def test_status_code_pag_edicao_concluida(resp_alteracao_newsletter, newsletter):
    """
    Certifica que, após alterada uma newsletter, a página de edição concluída é carregada com sucesso.
    """
    assert resp_alteracao_newsletter.status_code == 200
    assert resp_alteracao_newsletter.wsgi_request.path == f'/newsletter/adm/edicao/{newsletter.id}/'


def test_titulo_news_pag_edicao_concluida(resp_alteracao_newsletter, newsletter):
    """
    Certifica que, após editada uma newsletter, seu título e mensagem aparecem na página de edição concluída.
    """
    assert_contains(resp_alteracao_newsletter, f'A newsletter "<strong>{newsletter.title}</strong>" foi editada com s'
                                               f'ucesso.')


def test_alteracao_newsletter(newsletter,
                              client_usuario_logado_com_perm_edicao, subject):
    """
    Certifica de que uma alteração feita em uma newsletter é salva no banco de dados.
    """
    id_newsletter = newsletter.id
    client_usuario_logado_com_perm_edicao.post(
        reverse('newsletter:edicao', args=(id_newsletter,)),
        {'title': newsletter.title,
         'intro': 'Introdução alterada novamente',
         'content': 'Conteúdo alterado novamente',
         'subject': subject.pk,
         'author': newsletter.author,
         'slug': newsletter.slug,
         'criar_rascunho': 'NO'})
    news_editada = Newsletter.objects.get(id=newsletter.id)
    assert news_editada.intro == 'Introdução alterada novamente'
    assert news_editada.content == 'Conteúdo alterado novamente'
    assert news_editada.id == id_newsletter


def test_tentativa_alteracao_slug_repetida(newsletter,
                                           client_usuario_logado_com_perm_edicao, subject):
    """
    Certifica de que, ao tentar editar uma newsletter inserindo uma slug já existente no banco de dados,
    a mensagem de erro é exibida para o usuário.
    """
    id_newsletter = newsletter.id
    baker.make(Newsletter, content='Conteúdo', slug='slug-repetida')
    resp = client_usuario_logado_com_perm_edicao.post(
        reverse('newsletter:edicao', args=(id_newsletter,)),
        {'title': newsletter.title,
         'intro': newsletter.intro,
         'content': newsletter.content,
         'subject': subject.pk,
         'author': newsletter.author,
         'slug': 'slug-repetida',
         'criar_rascunho': 'NO'})
    assert_contains(resp, 'Newsletter com este Slug já existe.')


def test_criar_rascunho_email_apos_alteracao(newsletter,
                                             client_usuario_logado_com_perm_edicao, subject):
    """
    Certifica de que a função de criar rascunho de emails é chamada após a edição de uma
    newsletter. Para que seja chamada o usuário também deve selecionar a opção de criar rascunho.
    """
    facade.criar_rascunho = Mock()
    id_newsletter = newsletter.id
    client_usuario_logado_com_perm_edicao.post(
        reverse('newsletter:edicao', args=(id_newsletter,)),
        {'title': newsletter.title,
         'intro': newsletter.intro,
         'content': 'Teste criação rascunho de email',
         'subject': subject.pk,
         'author': newsletter.author,
         'slug': newsletter.slug,
         'criar_rascunho': 'YES'})
    facade.criar_rascunho.assert_called_once()


def test_nao_criar_rascunho_email_apos_alteracao(newsletter,
                                                 client_usuario_logado_com_perm_edicao, subject):
    """
    Certifica de que a função de criar rascunho de emails não é chamada após a edição de uma
    newsletter se o usuário não assinala a opção de criar rascunho.
    """
    facade.criar_rascunho = Mock()
    id_newsletter = newsletter.id
    client_usuario_logado_com_perm_edicao.post(
        reverse('newsletter:edicao', args=(id_newsletter,)),
        {'title': newsletter.title,
         'intro': newsletter.intro,
         'content': 'Teste não criação rascunho de email',
         'subject': subject.pk,
         'author': newsletter.author,
         'slug': newsletter.slug,
         'criar_rascunho': 'NO'})
    facade.criar_rascunho.assert_not_called()
