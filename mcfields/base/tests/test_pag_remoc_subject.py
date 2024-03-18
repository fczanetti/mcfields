import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.base.models import Subject
from mcfields.django_assertions import assert_contains
from mcfields.videos.models import Video


@pytest.fixture
def subject_para_remocao(db):
    """
    Cria um subject para tentativa de remoção.
    """
    sub = baker.make(Subject)
    return sub


@pytest.fixture
def video_para_remocao(subject_para_remocao):
    """
    Cria um vídeo relacionado com o subject para tentativa remoção.
    """
    video = baker.make(Video, subject=subject_para_remocao)
    return video


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
    assert_contains(resp_pag_remoc_subj_usuario_log_com_perm_rem, f'<a class="canc-removal-button" '
                                                                  f'href="{reverse("base:subjects")}">Cancelar</a>')


def test_tentativa_remocao_subject_com_conteudo_relacionado(
        video_para_remocao, client_usuario_logado_com_perm_remoc_subject):
    """
    Tenta acessar a página de remoção de algum assunto que possui algum conteúdo relacionado
    e certifica de que é direcionado para a página de remoção não permitida. Este teste também
    certifica de que o título da página e o título do assunto que seria removido estão presentes
    na página de remoção não permitida.
    """
    subject = video_para_remocao.subject
    resp = client_usuario_logado_com_perm_remoc_subject.get(reverse('base:remoc_subject', args=(subject.pk,)))
    assert_contains(resp, "<title>McField's - Remoção não permitida</title>")
    assert_contains(resp, f'O assunto "<strong>{subject.title}</strong>" não pode ser removido')
