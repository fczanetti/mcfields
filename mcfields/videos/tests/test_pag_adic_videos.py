import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_adic_video_usuario_nao_logado(client):
    """
    Realiza uma requisição na página de adição de vídeos com usuário não logado.
    """
    resp = client.get(reverse('videos:post'))
    return resp


@pytest.fixture
def resp_pag_adic_video_usuario_log_sem_perm(client_usuario_logado):
    """
    Realiza uma requisição na página de adição de vídeos com usuário logado sem permissão.
    """
    resp = client_usuario_logado.get(reverse('videos:post'))
    return resp


@pytest.fixture
def resp_pag_adic_video_usuario_log_com_perm(client_usuario_log_com_perm_adic_video):
    """
    Realiza uma requisição na página de adição de vídeos com usuário logado com permissão.
    """
    resp = client_usuario_log_com_perm_adic_video.get(reverse('videos:post'))
    return resp


def test_pag_adic_video_usuario_nao_logado(resp_pag_adic_video_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de adição de vídeos com
    usuário não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_adic_video_usuario_nao_logado.status_code == 302
    assert resp_pag_adic_video_usuario_nao_logado.url.startswith('/accounts/login/')


def test_pag_adic_video_usuario_logado_sem_perm(resp_pag_adic_video_usuario_log_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de vídeos com
    usuário logado sem permissão, o mesmo é redirecionado para a página de acesso negado.
    """
    assert resp_pag_adic_video_usuario_log_sem_perm.status_code == 302
    assert resp_pag_adic_video_usuario_log_sem_perm.url.startswith('/nao_permitido/')


def test_pag_adic_video_usuario_logado_com_perm(resp_pag_adic_video_usuario_log_com_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de vídeos com usuário logado
    e com permissão, a página é carregada com sucesso.
    """
    assert resp_pag_adic_video_usuario_log_com_perm.status_code == 200


def test_titulo_pag_adic_videos(resp_pag_adic_video_usuario_log_com_perm):
    """
    Certifica de que o título da página de adição de vídeos está
    presente e correto.
    """
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, "<title>McField's - Novo Vídeo</title>")


def test_form_pag_adic_videos(resp_pag_adic_video_usuario_log_com_perm):
    """
    Certifica de que os campos do formulário para adição de vídeos estão presentes.
    """
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<label for="id_title">Título:</label>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<input type="text" name="title" maxlength="64" '
                                                              'required id="id_title">')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<label for="id_description">Descrição:</label>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<textarea name="description" cols="40" rows="10" '
                                                              'required id="id_description">\n</textarea>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<label for="id_subject">Assunto:</label>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<select name="subject" required id="id_subject">')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<label for="id_platform_id">ID da plataforma:</label>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<input type="text" name="platform_id" maxlength="48" '
                                                              'required id="id_platform_id">')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<input type="text" name="slug" maxlength="64" '
                                                              'required id="id_slug">')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<label>Criar rascunho de email:</label>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<div id="id_criar_rascunho"><div>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<a class="canc-button" href="/videos/">Cancelar</a>')
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<button class="submit-button" '
                                                              'type="submit">Publicar</button>')


def test_titulo_form(resp_pag_adic_video_usuario_log_com_perm):
    """
    Certifica de que o título do formulário de está presente e
    indicando a adição de um novo vídeo.
    """
    assert_contains(resp_pag_adic_video_usuario_log_com_perm, '<h1 class="form-title">Novo Vídeo</h1>')
