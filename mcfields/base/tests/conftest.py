import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker
from mcfields.base.models import Subject


@pytest.fixture
def subject(db):
    """
    Cria e retorna um subject.
    """
    sub = baker.make(Subject)
    return sub


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
def usuario_senha_plana_com_perm_edic_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de edição de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='change_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_edic_subject = usuario_senha_plana
    return usuario_com_perm_edic_subject


@pytest.fixture
def client_usuario_logado_com_perm_edic_subject(client, usuario_senha_plana_com_perm_edic_subject):
    """
    Cria um cliente com usuário logado e com permissão de edição de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_edic_subject)
    return client
