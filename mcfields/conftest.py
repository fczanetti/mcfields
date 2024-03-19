import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from mcfields.base.models import Subject
from mcfields.servicos.models import Service


@pytest.fixture
def usuario_senha_plana(db):
    """
    Cria um usuário e define uma senha acessível para este.
    """
    user = baker.make(get_user_model())
    senha = 'senha'
    user.set_password(senha)
    user.save()
    user.senha_plana = senha
    return user


@pytest.fixture
def client_usuario_logado(client, usuario_senha_plana):
    """
    Cria um usuário logado na plataforma.
    """
    client.force_login(usuario_senha_plana)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_adic_serv(usuario_senha_plana):
    """
    Cria um usuário com permissão de adição de serviços.
    """
    content_type = ContentType.objects.get_for_model(Service)
    permission = Permission.objects.get(codename='add_service', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_adicao = usuario_senha_plana
    return usuario_com_perm_adicao


@pytest.fixture
def client_usuario_log_com_perm_adic_serv(usuario_senha_plana_com_perm_adic_serv, client):
    """
    Cria um client com usuário logado e permissão de adição de serviços.
    """
    client.force_login(usuario_senha_plana_com_perm_adic_serv)
    return client


@pytest.fixture
def subject(db):
    """
    Cria e retorna um subject.
    """
    sub = baker.make(Subject)
    return sub
