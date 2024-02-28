import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker


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
