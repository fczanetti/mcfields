import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_remoc_subj_usuario_nao_log(client, subject):
    """
    Realiza uma requisição na página de confirmação de
    remoção de assunto com usuário não logado.
    """
    resp = client.get(reverse('base:remoc_subject', args=(subject.pk,)))
    return resp


@pytest.fixture
def resp_pag_remoc_subj_usuario_log_sem_perm_rem(client_usuario_logado, subject):
    """
    Realiza uma requisição na página de confirmação de
    remoção de assunto com usuário logado sem permissão de remoção.
    """
    resp = client_usuario_logado.get(reverse('base:remoc_subject', args=(subject.pk,)))
    return resp


@pytest.fixture
def resp_pag_remoc_subj_usuario_log_com_perm_rem(client_usuario_logado_com_perm_remoc_subject, subject):
    """
    Realiza uma requisição na página de confirmação de
    remoção de assunto com usuário logado com permissão de remoção.
    """
    resp = client_usuario_logado_com_perm_remoc_subject.get(reverse('base:remoc_subject', args=(subject.pk,)))
    return resp


def test_redirect_pag_remoc_subject_usuario_nao_log(resp_pag_remoc_subj_usuario_nao_log):
    """
    Certifica de que, ao tentar acessar a página de remoção de assuntos com
    usuário não logado, este é redirecionado para a página de login.
    """
    assert resp_pag_remoc_subj_usuario_nao_log.status_code == 302
    assert resp_pag_remoc_subj_usuario_nao_log.url.startswith('/accounts/login/')


def test_redirect_pag_remoc_subject_usuario_log_sem_perm(resp_pag_remoc_subj_usuario_log_sem_perm_rem):
    """
    Certifica de que, ao tentar acessar a página de remoção de assuntos com
    usuário logado sem permissão de remoção, este é redirecionado para a página de login.
    """
    assert resp_pag_remoc_subj_usuario_log_sem_perm_rem.status_code == 302
    assert resp_pag_remoc_subj_usuario_log_sem_perm_rem.url.startswith('/nao_permitido/')


def test_redirect_pag_remoc_subject_usuario_log_com_perm(resp_pag_remoc_subj_usuario_log_com_perm_rem):
    """
    Certifica de que, ao tentar acessar a página de remoção de assuntos com
    usuário logado com permissão de remoção, a página é carregada com sucesso.
    """
    assert resp_pag_remoc_subj_usuario_log_com_perm_rem.status_code == 200


def test_titulo_subject_pag_remocao(resp_pag_remoc_subj_usuario_log_com_perm_rem, subject):
    """
    Certifica de que, ao acessar a página de confirmação de remoção, o
    título do assunto a ser removido está presente.
    """
    assert_contains(resp_pag_remoc_subj_usuario_log_com_perm_rem, subject.title)


def test_bot_cancelar_pag_remocao_subject(resp_pag_remoc_subj_usuario_log_com_perm_rem, subject):
    """
    Certifica de que o botão de cancelar remoção está presente e direcionando
    para a página de índice de assuntos.
    """
    assert_contains(resp_pag_remoc_subj_usuario_log_com_perm_rem, f'<a id="canc-removal-button" '
                                                                  f'href="{reverse("base:subjects")}">Cancelar</a>')
