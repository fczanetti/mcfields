import pytest
from django.urls import reverse

from mcfields.base.models import Contact
from mcfields.django_assertions import assert_false, assert_contains


@pytest.fixture
def remocao_mensagem(client_usuario_logado_com_perm_remoc_contact, mensagem):
    """
    Remove uma mensagem (contact).
    """
    resp = client_usuario_logado_com_perm_remoc_contact.post(
        reverse('base:remoc_contact', args=(mensagem.pk,)))
    return resp


def test_mensagem_removida(remocao_mensagem, mensagem):
    """
    Certifica de que a mensagem foi removida do banco de dados.
    """
    assert_false(Contact.objects.filter(id=mensagem.pk).exists())


def test_titulo_pag_remocao_concluida(remocao_mensagem):
    """
    Certifica de que o título da página de remoção concluída está presente.
    """
    assert_contains(remocao_mensagem, "<title>McField's - Remoção concluída</title>")


def test_nome_mensagem_pag_remocao_concluida(remocao_mensagem, mensagem):
    """
    Certifica de que o nome do remetente da mensagem está presente
    na página de remoção concluída.
    """
    assert_contains(remocao_mensagem, mensagem.name)
