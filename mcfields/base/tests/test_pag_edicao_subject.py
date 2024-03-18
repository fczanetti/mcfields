import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_edic_subject_usuario_nao_logado(client, subject):
    """
    Realiza uma requisição na página de edição de assuntos
    com usuário não logado.
    """
    resp = client.get(reverse('base:edic_subject', args=(subject.pk,)))
    return resp


@pytest.fixture
def resp_pag_edic_subject_usuario_logado_sem_perm(client_usuario_logado, subject):
    """
    Realiza uma requisição na página de edição de assuntos
    com usuário logado sem permissão de edição.
    """
    resp = client_usuario_logado.get(reverse('base:edic_subject', args=(subject.pk,)))
    return resp


@pytest.fixture
def resp_pag_edic_subject_usuario_log_com_perm(client_usuario_logado_com_perm_edic_subject, subject):
    """
    Realiza uma requisição na página de edição de assuntos
    com usuário logado e com permissão de edição.
    """
    resp = client_usuario_logado_com_perm_edic_subject.get(reverse('base:edic_subject', args=(subject.pk,)))
    return resp


def test_redirect_pag_edicao_subject_usuario_nao_log(resp_pag_edic_subject_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de edição de assuntos com
    usuário não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_edic_subject_usuario_nao_logado.status_code == 302
    assert resp_pag_edic_subject_usuario_nao_logado.url.startswith('/accounts/login/')


def test_acesso_neg_pag_edicao_subject_usuario_log_sem_perm(resp_pag_edic_subject_usuario_logado_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de edição de assuntos com
    usuário logado sem permissão, o mesmo é redirecionado para a página de acesso negado.
    """
    assert resp_pag_edic_subject_usuario_logado_sem_perm.status_code == 302
    assert resp_pag_edic_subject_usuario_logado_sem_perm.url.startswith('/nao_permitido/')


def test_status_code_pag_edicao_subject(resp_pag_edic_subject_usuario_log_com_perm):
    """
    Certifica de que, ao tentar acessar a página de edição de assuntos com
    usuário logado com permissão, a página é carregada com sucesso.
    """
    assert resp_pag_edic_subject_usuario_log_com_perm.status_code == 200


def test_infos_subject_pag_edicao(resp_pag_edic_subject_usuario_log_com_perm, subject):
    """
    Certifica de que as informções do subject a ser editado
    estão presentes na página de edição.
    """
    assert_contains(resp_pag_edic_subject_usuario_log_com_perm, f'<input type="text" name="title" '
                                                                f'value="{subject.title}" maxlength="64" required '
                                                                f'id="id_title">')
    assert_contains(resp_pag_edic_subject_usuario_log_com_perm, subject.description)
    assert_contains(resp_pag_edic_subject_usuario_log_com_perm, subject.slug)


def test_titulo_pag_edicao_subject(resp_pag_edic_subject_usuario_log_com_perm):
    """
    Certifica de que o título da página de edição de serviços
    está presente e correto.
    """
    assert_contains(resp_pag_edic_subject_usuario_log_com_perm, "<title>McField's - Edição de Assunto</title>")


def test_titulo_form(resp_pag_edic_subject_usuario_log_com_perm, subject):
    """
    Certifica de que o título do formulário está presente e
    informando a edição de um assunto existente.
    """
    assert_contains(resp_pag_edic_subject_usuario_log_com_perm, f'<h1 class="form-title">Edição do Assunto '
                                                                f'"{subject.title}"</h1>')
