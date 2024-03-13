import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mcfields.videos.models import Video


@pytest.fixture
def usuario_senha_plana_com_perm_adic_video(usuario_senha_plana):
    """
    Cria um usuário com permissão de adição de vídeos.
    """
    content_type = ContentType.objects.get_for_model(Video)
    permission = Permission.objects.get(codename='add_video', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_adicao = usuario_senha_plana
    return usuario_com_perm_adicao


@pytest.fixture
def client_usuario_log_com_perm_adic_video(usuario_senha_plana_com_perm_adic_video, client):
    """
    Cria um client com usuário logado e permissão de adição de videos.
    """
    client.force_login(usuario_senha_plana_com_perm_adic_video)
    return client
