import pytest
from model_bakery import baker
from mcfields.newsletter.models import Newsletter
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


@pytest.fixture
def newsletter(subject, db):
    """
    Cria uma newsletter para que sua página de detalhes seja acessada.
    """
    news = baker.make(Newsletter, content='Texto da newsletter', subject=subject)
    return news


@pytest.fixture
def usuario_senha_plana_com_perm_postagem(usuario_senha_plana):
    """
    Cria um usuário com permissão de postagem de newsletters a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Newsletter)
    permission = Permission.objects.get(codename='add_newsletter', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_postagem = usuario_senha_plana
    return usuario_com_perm_postagem


@pytest.fixture
def client_usuario_logado_com_perm_postagem(client, usuario_senha_plana_com_perm_postagem):
    """
    Cria um cliente com usuário logado e com permissão de postagem de newsletters.
    """
    client.force_login(usuario_senha_plana_com_perm_postagem)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_edicao(usuario_senha_plana):
    """
    Cria um usuário com permissão de edição de newsletters a partir do usuario_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Newsletter)
    permission = Permission.objects.get(codename='change_newsletter', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_edicao = usuario_senha_plana
    return usuario_com_perm_edicao


@pytest.fixture
def client_usuario_logado_com_perm_edicao(client, usuario_senha_plana_com_perm_edicao):
    """
    Cria um client com usuário logado e permissão de edição de newsletter.
    """
    client.force_login(usuario_senha_plana_com_perm_edicao)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_remocao(usuario_senha_plana):
    """
    Cria um usuário com permissão de remoção de newsletters a partir do usuario_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Newsletter)
    permission = Permission.objects.get(codename='delete_newsletter', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_remocao = usuario_senha_plana
    return usuario_com_perm_remocao


@pytest.fixture
def client_usuario_logado_com_perm_remocao(client, usuario_senha_plana_com_perm_remocao):
    """
    Cria um client com usuário logado e permissão de remoção de newsletter.
    """
    client.force_login(usuario_senha_plana_com_perm_remocao)
    return client
