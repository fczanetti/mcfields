import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from mcfields.base.models import Subject


@pytest.fixture
def usuario_senha_plana_com_perm_adic_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de adição de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='add_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_adic_subject = usuario_senha_plana
    return usuario_com_perm_adic_subject


@pytest.fixture
def client_usuario_logado_com_perm_adic_subject(client, usuario_senha_plana_com_perm_adic_subject):
    """
    Cria um cliente com usuário logado e com permissão de adição de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_adic_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de visualização de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='view_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_view_subject = usuario_senha_plana
    return usuario_com_perm_view_subject


@pytest.fixture
def client_usuario_logado_com_perm_view_subject(client, usuario_senha_plana_com_perm_view_subject):
    """
    Cria um cliente com usuário logado e com permissão de visualização de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_view_subject)
    return client
