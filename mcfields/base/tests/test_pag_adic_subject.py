import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_adic_subject_usuario_nao_log(client):
    """
    Realiza uma requisição na página de adição de assuntos.
    """
    resp = client.get(reverse('base:adic_subject'))
    return resp


@pytest.fixture
def resp_pag_adic_subject_usuario_log_sem_perm(client_usuario_logado):
    """
    Realiza uma requisição na página de adição de assuntos com
    usuário logado sem permissão de adição.
    """
    resp = client_usuario_logado.get(reverse('base:adic_subject'))
    return resp


@pytest.fixture
def resp_pag_adic_subject_usuario_log_com_perm(client_usuario_logado_com_perm_adic_subject):
    """
    Realiza uma requisição na página de adição de assuntos com
    usuário logado com permissão de adição.
    """
    resp = client_usuario_logado_com_perm_adic_subject.get(reverse('base:adic_subject'))
    return resp


def test_redirect_pag_adic_subject_usuario_nao_log(resp_pag_adic_subject_usuario_nao_log):
    """
    Certifica de que, ao tentar acessar a página de adição de assuntos com usuário
    não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_adic_subject_usuario_nao_log.status_code == 302
    assert resp_pag_adic_subject_usuario_nao_log.url.startswith('/accounts/login/')


def test_acesso_neg_pag_adic_subject_usuario_log_sem_perm(resp_pag_adic_subject_usuario_log_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de assuntos com usuário
    logado sem permissão de adição, o mesmo é redirecionado para a página de acesso negado.
    """
    assert resp_pag_adic_subject_usuario_log_sem_perm.status_code == 302
    assert resp_pag_adic_subject_usuario_log_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_adic_subject(resp_pag_adic_subject_usuario_log_com_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de assuntos com usuário
    logado com permissão de adição, a página é carregada com sucesso.
    """
    assert resp_pag_adic_subject_usuario_log_com_perm.status_code == 200


def test_titulo_pag_adic_subject(resp_pag_adic_subject_usuario_log_com_perm):
    """
    Certifica de que o título da página de adição de subjects (assuntos) está presente e correto.
    """
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, "<title>McField's - Novo Assunto</title>")


def test_form_pag_adic_subject(resp_pag_adic_subject_usuario_log_com_perm):
    """
    Certifica de que os campos do formulário de adição de assunto estão presentes.
    """
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, '<label for="id_title">Título:</label>')
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, '<input type="text" name="title" maxlength="64" '
                                                                'required id="id_title">')
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, '<label for="id_description">Descrição:</label>')
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, '<textarea name="description" cols="40" rows="10" '
                                                                'maxlength="256" required '
                                                                'id="id_description">\n</textarea>')
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, '<input type="text" name="slug" maxlength="64" '
                                                                'required id="id_slug">')
    assert_contains(resp_pag_adic_subject_usuario_log_com_perm, 'Cancelar')
