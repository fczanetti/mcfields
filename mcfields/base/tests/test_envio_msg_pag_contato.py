from unittest.mock import Mock

import pytest
from django.urls import reverse

from mcfields import settings
from mcfields.base import facade
from mcfields.base.models import Contact
from mcfields.django_assertions import assert_contains, assert_true


@pytest.fixture
def resp_envio_mensagem(client, db):
    """
    Envia uma mensagem através do formulário de contato.
    """
    facade.enviar_mensagem = Mock()
    resp = client.post(reverse('base:contato'), {'name': 'Fabio', 'email': 'teste@teste.com',
                                                 'subject': 'Assunto da mensagem',
                                                 'message': 'Mensagem', 'agree_with_policy': True})
    return resp


@pytest.fixture
def resp_nao_envio_mensagem(client, db):
    """
    Tenta enviar uma mensagem sem concordar com a política de privacidade.
    """
    facade.enviar_mensagem = Mock()
    resp = client.post(reverse('base:contato'), {'name': 'Fabio', 'email': 'teste@teste.com',
                                                 'subject': 'Assunto da mensagem',
                                                 'message': 'Discordo da política', 'agree_with_policy': False})
    return resp


def test_pag_envio_concluido(resp_envio_mensagem):
    """
    Certifica de que a página de envio de mensagem concluído é carregada com sucesso
    após o envio de uma mensagem pelo formulário de contato.
    """
    assert resp_envio_mensagem.status_code == 200
    assert_contains(resp_envio_mensagem, "<title>McField's - Mensagem enviada</title>")
    assert_contains(resp_envio_mensagem, 'Sua mensagem foi enviada com sucesso, retornaremos assim que possível. '
                                         'Obrigado!')


def test_funcao_enviar_mensagem(client, db):
    """
    Certifica de que a função de enviar mensagem foi chamada após o envio de uma mensagem
    através do formulário de contato.
    """
    facade.enviar_mensagem = Mock()
    client.post(reverse('base:contato'), {'name': 'Fabio', 'email': 'teste@teste.com',
                                          'subject': 'Assunto da mensagem',
                                          'message': 'Mensagem', 'agree_with_policy': True})
    facade.enviar_mensagem.assert_called_once_with(
        key=settings.SENDGRID_API_KEY, name='Fabio', email='teste@teste.com', subject='Assunto da mensagem',
        message='Mensagem', from_email=settings.FROM_EMAIL, to_email=settings.TO_EMAIL
    )


def test_funcao_enviar_mensagem_nao_chamada(resp_nao_envio_mensagem):
    """
    Certifica de que a função de enviar mensagem não foi chamada após tentativa de envio de mensagem
    sem concordar com a política de privacidade.
    """
    facade.enviar_mensagem = Mock()
    facade.enviar_mensagem.assert_not_called()


def test_erro_ao_tent_env_msg_sem_conc_com_politica(resp_nao_envio_mensagem):
    """
    Certifica de que a mensagem de erro é exibida para o usuário que tenta
    enviar mensagem sem concordar com a política de privacidade.
    """
    assert_contains(resp_nao_envio_mensagem, 'Você deve concordar com nossa política de privacidade.')


def test_mensagem_salva(resp_envio_mensagem):
    """
    Certifica de que, após enviada uma mensagem via formulário de contato, esta
    é salva no banco de dados.
    """
    assert_true(Contact.objects.filter(subject='Assunto da mensagem').exists())
