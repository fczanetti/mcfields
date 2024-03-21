from unittest.mock import Mock

from django.urls import reverse
from model_bakery import baker

from mcfields.django_assertions import assert_contains
from mcfields.videos import facade
from mcfields.videos.models import Video


def test_edicao_de_video(client_usuario_log_com_perm_edic_video, video):
    """
    Certifica de que as alterações em um vídeo são de fato salvas
    no banco de dados.
    """
    client_usuario_log_com_perm_edic_video.post(reverse('videos:edicao', args=(video.pk,)),
                                                {'title': 'Título alterado',
                                                 'description': 'Descrição alterada',
                                                 'subject': video.subject.pk,
                                                 'platform_id': video.platform_id,
                                                 'slug': video.slug,
                                                 'criar_rascunho': 'NO'})
    vid_alterado = Video.objects.get(id=video.pk)
    assert vid_alterado.title == 'Título alterado'
    assert vid_alterado.description == 'Descrição alterada'


def test_pag_edicao_concluida(video, client_usuario_log_com_perm_edic_video):
    """
    Certifica de que após a edição do vídeo o usuário é levado para a
    página de edição concluída com sucesso.
    """
    resp = client_usuario_log_com_perm_edic_video.post(reverse('videos:edicao', args=(video.pk,)),
                                                       {'title': 'Título alterado novamente',
                                                        'description': 'Descrição alterada',
                                                        'subject': video.subject.pk,
                                                        'platform_id': video.platform_id,
                                                        'slug': video.slug,
                                                        'criar_rascunho': 'NO'})
    video_alterado = Video.objects.get(title='Título alterado novamente')
    assert_contains(resp, f'O vídeo "<strong>{video_alterado.title}</strong>" foi editado com sucesso.')


def test_tentativa_edicao_slug_repetida(video, client_usuario_log_com_perm_edic_video, subject):
    """
    Certifica de que, ao tentar editar um vídeo inserindo uma slug já existente no banco de dados,
    a mensagem de erro é exibida para o usuário.
    """
    baker.make(Video, subject=subject, slug='slug-repetida')
    resp = client_usuario_log_com_perm_edic_video.post(reverse('videos:edicao', args=(video.pk,)),
                                                       {'title': video.title,
                                                        'description': video.description,
                                                        'subject': video.subject.pk,
                                                        'platform_id': video.platform_id,
                                                        'slug': 'slug-repetida',
                                                        'criar_rascunho': 'NO'})
    assert_contains(resp, 'Video com este Slug já existe.')


def test_criar_rascunho_email_apos_edicao(video, client_usuario_log_com_perm_edic_video, subject):
    """
    Certifica de que a função de criar rascunho de email é chamada após a edição de um vídeo. Para
    que seja chamada é necessário que o usuário tenha assinalado a opção de criar rascunho.
    """
    facade.criar_rascunho = Mock()
    client_usuario_log_com_perm_edic_video.post(reverse('videos:edicao', args=(video.pk,)),
                                                {'title': 'Teste enviar rascunho de email',
                                                 'description': video.description,
                                                 'subject': video.subject.pk,
                                                 'platform_id': video.platform_id,
                                                 'slug': video.slug,
                                                 'criar_rascunho': 'YES'})
    facade.criar_rascunho.assert_called_once()


def test_nao_criar_rascunho_email_apos_edicao(video, client_usuario_log_com_perm_edic_video, subject):
    """
    Certifica de que a função de criar rascunho de email não é chamada após a edição de um vídeo
    se o usuário não assinalou a opção de criação de rascunho.
    """
    facade.criar_rascunho = Mock()
    client_usuario_log_com_perm_edic_video.post(reverse('videos:edicao', args=(video.pk,)),
                                                {'title': 'Teste não enviar rascunho de email',
                                                 'description': video.description,
                                                 'subject': video.subject.pk,
                                                 'platform_id': video.platform_id,
                                                 'slug': video.slug,
                                                 'criar_rascunho': 'NO'})
    facade.criar_rascunho.assert_not_called()
