import pytest
from django.urls import reverse
from mcfields.base.models import Subject
from mcfields.django_assertions import assert_false, assert_contains


@pytest.fixture
def remocao_assunto(client_usuario_logado_com_perm_remoc_subject, subject):
    """
    Remove um assunto.
    """
    resp = client_usuario_logado_com_perm_remoc_subject.post(
        reverse('base:remoc_subject', args=(subject.pk,)))
    return resp


def test_assunto_removido(remocao_assunto, subject):
    """
    Certifica de que o assunto foi removido do banco de dados.
    """
    assert_false(Subject.objects.filter(id=subject.pk).exists())


def test_titulo_assunto_pag_remocao_concluida(remocao_assunto, subject):
    """
    Certifica de que o título do assunto removido está
    presente na página de remoção concluída.
    """
    assert_contains(remocao_assunto, subject.title)
