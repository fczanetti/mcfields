from unittest.mock import Mock
from django.urls import reverse
from mcfields.base import facade


def test_inscricao_email_concluida(client):
    """
    Certifica de que a função de cadastrar_email é chamada ao realizar uma inscrição.
    """
    response = Mock()
    response.body = b''
    facade.checar_email_descadastrado = Mock(return_value=response)
    facade.cadastrar_email = Mock()
    client.post(reverse('base:inscricao_email'), {'email': 'fabio@hotmail.com'})
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
    client.post(reverse('base:inscricao_email'), {'email': 'email@email.com'})
    facade.checar_email_descadastrado.assert_called_once()
    facade.remover_da_lista_desc.assert_called_once()
    facade.cadastrar_email.assert_not_called()
