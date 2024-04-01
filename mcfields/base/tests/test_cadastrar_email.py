from unittest.mock import Mock
from django.urls import reverse
from mcfields.base import facade
from mcfields.django_assertions import assert_contains


def test_inscricao_email_concluida(client):
    """
    Certifica de que a função de cadastrar_email é chamada ao realizar uma inscrição.
    """
    response = Mock()
    response.body = b''
    facade.checar_email_descadastrado = Mock(return_value=response)
    facade.cadastrar_email = Mock()
    client.post(reverse('base:inscricao_email'), {'email': 'fabio@hotmail.com', 'policy_agreement': True})
    facade.cadastrar_email.assert_called_once()


def test_remocao_email_lista_descadastrados(client):
    """
    Certifica de que, caso um email esteja na lista de descadastrados e o usuário tente cadastrá-lo
    cadastrar novamente, o email é removido da lista de descadastrados através da função
    remover_da_lista_desc(). Este teste também garante que a função cadastrar_email() não é chamada.
    """
    response = Mock()
    response.body = b'email@email.com'
    facade.checar_email_descadastrado = Mock(return_value=response)
    facade.remover_da_lista_desc = Mock()
    facade.cadastrar_email = Mock()
    client.post(reverse('base:inscricao_email'), {'email': 'email@email.com', 'policy_agreement': True})
    facade.checar_email_descadastrado.assert_called_once()
    facade.remover_da_lista_desc.assert_called_once()
    facade.cadastrar_email.assert_not_called()


def test_inscricao_email_nao_concluida(client):
    """
    Certifica de que as funções de cadastrar_email não são chamadas ao realizar uma inscrição
    se o usuário não concordar com a política de privacidade.
    """
    response = Mock()
    response.body = b''
    facade.checar_email_descadastrado = Mock(return_value=response)
    facade.cadastrar_email = Mock()
    client.post(reverse('base:inscricao_email'), {'email': 'fabio@hotmail.com', 'policy_agreement': False})
    facade.cadastrar_email.assert_not_called()
    facade.checar_email_descadastrado.assert_not_called()


def test_mensagens_erro_ao_cadastrar_email(client):
    """
    Certifica de que as mensagens de erro aparecem para o usuário caso o formulário
    de cadastro de email não seja preenchido com dados válidos. Considerando email
    não preenchido e usuário que não está de acordo com a política de privacidade.
    """
    response = Mock()
    response.body = b''
    facade.checar_email_descadastrado = Mock(return_value=response)
    facade.cadastrar_email = Mock()
    resp = client.post(reverse('base:inscricao_email'), {'policy_agreement': False})
    assert_contains(resp, 'É necessário informar um email para cadastro.')
    assert_contains(resp, 'É necessário concordar com nossa política de privacidade.')


def test_mensagens_erro_ao_cadastrar_email_2(client):
    """
    Certifica de que as mensagens de erro aparecem para o usuário caso o formulário
    de cadastro de email não seja preenchido com dados válidos. Considerando email
    preenchido incorretamente.
    """
    response = Mock()
    response.body = b''
    facade.checar_email_descadastrado = Mock(return_value=response)
    facade.cadastrar_email = Mock()
    resp = client.post(reverse('base:inscricao_email'), {'email': 'fabiohotmail.com', 'policy_agreement': True})
    assert_contains(resp, 'Informe um endereço de email válido.')
