from unittest.mock import Mock

import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields import settings
from mcfields.base.models import Assunto
from mcfields.django_assertions import assert_contains, assert_false, assert_true
from mcfields.videos import views
from mcfields.videos.models import Video


@pytest.fixture
def assunto(db):
    """
    Cria um assunto para ser utilizado na criação de vídeos.
    """
    subject = baker.make(Assunto, title='assunto titulo', slug='assunto-titulo')
    return subject


@pytest.fixture
def resp_adicao_video(client_usuario_log_com_perm_adic_video, assunto):
    """
    Adiciona um vídeo novo na plataforma.
    """
    views.criar_rascunho = Mock()
    resp = client_usuario_log_com_perm_adic_video.post(reverse('videos:post'),
                                                       {'title': 'Título do vídeo',
                                                        'description': 'Descrição do vídeo',
                                                        'subject': assunto.pk,
                                                        'platform_id': 'abcde',
                                                        'slug': 'titulo-do-video',
                                                        'criar_rascunho': 'YES'})
    return resp


@pytest.fixture
def resp_adicao_video_slug_repetida(client_usuario_log_com_perm_adic_video, assunto):
    """
    Adiciona um vídeo novo na plataforma.
    """
    views.criar_rascunho = Mock()
    baker.make(Video, subject=assunto, slug='teste-slug-repetida')
    resp = client_usuario_log_com_perm_adic_video.post(reverse('videos:post'),
                                                       {'title': 'Título slug repetida',
                                                        'description': 'Descrição slug repetida',
                                                        'subject': assunto.pk,
                                                        'platform_id': 'abcde',
                                                        'slug': 'teste-slug-repetida',
                                                        'criar_rascunho': 'YES'})
    return resp


def test_pag_adicao_concluida(resp_adicao_video):
    """
    Certifica de que, após a adição de um vídeo com sucesso, o usuário
    é direcionado para a página de adição concluída.
    """
    assert_contains(resp_adicao_video, 'O vídeo "<strong>Título do vídeo</strong>" foi adicionado com sucesso.')


def test_video_salvo(resp_adicao_video):
    """
    Certifica de que o vídeo foi salvo no banco de dados.
    """
    saved = False
    if Video.objects.get(slug='titulo-do-video'):
        saved = True
    assert_true(saved)


def test_adic_video_slug_repetida(resp_adicao_video_slug_repetida):
    """
    Certifica de que, ao tentar adicionar algum vídeo com slug repetida, o
    erro aparece na tela.
    """
    assert resp_adicao_video_slug_repetida.wsgi_request.path == '/videos/adm/post'
    assert_contains(resp_adicao_video_slug_repetida, 'Video com este Slug já existe.')


def test_video_slug_repetida_nao_salvo(resp_adicao_video_slug_repetida):
    """
    Certifica de que o vídeo com slug repetida não foi salvo no banco de dados.
    """
    saved = False
    if Video.objects.filter(title='Título slug repetida'):
        saved = True
    assert_false(saved)


def test_funcao_enviar_rascunho_email_chamada(client_usuario_log_com_perm_adic_video, assunto):
    """
    Certifica de que a função de envio de rascunho de emails foi chamada ao salvar o vídeo.
    """
    views.criar_rascunho = Mock()
    client_usuario_log_com_perm_adic_video.post(reverse('videos:post'),
                                                {'title': 'Criar email',
                                                 'description': 'Descrição do vídeo',
                                                 'subject': assunto.pk,
                                                 'platform_id': 'abcde',
                                                 'slug': 'criar-email',
                                                 'criar_rascunho': 'YES'})
    views.criar_rascunho.assert_called_once_with(key=settings.SENDGRID_API_KEY,
                                                 titulo='Criar email',
                                                 list_id=settings.SENDGRID_LIST_ID,
                                                 design_id=settings.SENDGRID_VIDEO_DESIGN_ID)


def test_funcao_enviar_rascunho_email_nao_chamada(client_usuario_log_com_perm_adic_video, assunto):
    """
    Certifica de que a função de envio de rascunho de emails não foi chamada ao salvar o vídeo.
    """
    views.criar_rascunho = Mock()
    client_usuario_log_com_perm_adic_video.post(reverse('videos:post'),
                                                {'title': 'Não criar email',
                                                 'description': 'Descrição do vídeo',
                                                 'subject': assunto.pk,
                                                 'platform_id': 'abcde',
                                                 'slug': 'nao-criar-email',
                                                 'criar_rascunho': 'NO'})
    views.criar_rascunho.assert_not_called()
