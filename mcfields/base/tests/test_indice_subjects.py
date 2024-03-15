import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.base.models import Subject
from mcfields.django_assertions import assert_contains
from mcfields.videos.models import Video


@pytest.fixture
def subjects(db):
    """
    Cria alguns assuntos.
    """
    subs = baker.make(Subject, _quantity=2)
    return subs


@pytest.fixture
def videos(subjects, db):
    """
    Cria alguns vídeos relacionados com os assuntos
    para serem exibidos no índice.
    """
    vid = []
    for sub in subjects:
        vid.extend(baker.make(Video, subject=sub, _quantity=2))
    return vid


@pytest.fixture
def resp_indice_subject_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de índice de assuntos
    com usuário não logado.
    """
    resp = client.get(reverse('base:subjects'))
    return resp


@pytest.fixture
def resp_indice_subject_usuario_log_sem_perm_view(client_usuario_logado):
    """
    Realiza uma requisição na página de índice de assuntos
    com usuário logado sem permissão de visualização.
    """
    resp = client_usuario_logado.get(reverse('base:subjects'))
    return resp


@pytest.fixture
def resp_indice_subject_usuario_log_com_perm_view(client_usuario_logado_com_perm_view_subject, videos):
    """
    Realiza uma requisição na página de índice de assuntos
    com usuário logado com permissão de visualização.
    """
    resp = client_usuario_logado_com_perm_view_subject.get(reverse('base:subjects'))
    return resp


def test_redirect_indice_subjects_usuario_nao_log(resp_indice_subject_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de índice de assuntos com
    usuário não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_indice_subject_usuario_nao_logado.status_code == 302
    assert resp_indice_subject_usuario_nao_logado.url.startswith('/accounts/login/')


def test_redirect_indice_subjects_usu_log_sem_perm_view(resp_indice_subject_usuario_log_sem_perm_view):
    """
    Certifica de que, ao tentar acessar a página de índice de assuntos com
    usuário logado sem permissão de visualização, o mesmo é redirecionado para a página de acesso negado.
    """
    assert resp_indice_subject_usuario_log_sem_perm_view.status_code == 302
    assert resp_indice_subject_usuario_log_sem_perm_view.url.startswith('/nao_permitido/')


def test_status_code_indice_subjects(resp_indice_subject_usuario_log_com_perm_view):
    """
    Certifica de que, ao tentar acessar a página de índice de assuntos com usuário
    logado e com permissão de visualização, a página é carregada com sucesso.
    """
    assert resp_indice_subject_usuario_log_com_perm_view.status_code == 200


def test_titulo_indice_assuntos(resp_indice_subject_usuario_log_com_perm_view):
    """
    Certifica de que o título da página de índice de assuntos
    está presente e correto.
    """
    assert_contains(resp_indice_subject_usuario_log_com_perm_view, "<title>McField's - Assuntos</title>")


def test_subjects_presentes_no_indice(resp_indice_subject_usuario_log_com_perm_view, subjects):
    """
    Certifica de que os subjects (assuntos) criados estão presentes no índice.
    """
    for sub in subjects:
        assert_contains(resp_indice_subject_usuario_log_com_perm_view, sub.title)


def test_videos_presentes_no_indice_de_assuntos(resp_indice_subject_usuario_log_com_perm_view, videos):
    """
    Certifica de que os vídeos estão presentes no índice de assuntos.
    """
    for video in videos:
        assert_contains(resp_indice_subject_usuario_log_com_perm_view, video.title)