import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_login_page(client):
    """
    Realiza uma requisição na página de login.
    """
    response = client.get(reverse('base:login'))
    return response


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
def login(client, usuario_senha_plana):
    """
    Realiza o login com o usuário criado.
    """
    response = client.post(reverse('base:login'), {'username': usuario_senha_plana.get_username(),
                                                   'password': usuario_senha_plana.senha_plana})
    return response


def test_status_code_login_page(resp_login_page):
    """
    Certifica que a página de login foi carregada com sucesso.
    """
    assert resp_login_page.status_code == 200


def test_login_form(resp_login_page):
    """
    Certifica de que o formulário e seus componentes estão presentes na página de login.
    """
    assert_contains(resp_login_page, '<label for="id_username">Endereço de email:</label>')
    assert_contains(resp_login_page, '<input type="text" name="username" autofocus autocapitalize="none" '
                                     'autocomplete="username" maxlength="254" required id="id_username">')
    assert_contains(resp_login_page, '<label for="id_password">Senha:</label>')
    assert_contains(resp_login_page, '<input type="password" name="password" autocomplete="current-password" required '
                                     'id="id_password">')
    assert_contains(resp_login_page, '<input type="submit" value="Login" id="login-button">')


def test_login_redirect(login):
    """
    Certifica de que, após o login, o usuário é redirecionado para a página inicial.
    """
    assert login.status_code == 302
    assert login.url == reverse('base:home')
