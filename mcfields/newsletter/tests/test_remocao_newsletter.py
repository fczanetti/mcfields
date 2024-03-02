import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_false, assert_contains
from mcfields.newsletter.models import Newsletter


@pytest.fixture
def resp_remocao_newsletter(client_usuario_logado_com_perm_remocao, newsletter):
    """
    Remove uma newsletter e retorna a resposta da remoção.
    """
    resp = client_usuario_logado_com_perm_remocao.post(
        reverse('newsletter:remocao', args=(newsletter.id,)))
    return resp


def test_titulos_pag_remocao_concluida(resp_remocao_newsletter, newsletter):
    """
    Certifica que os títulos da newsletter removida e o título da página
    estão presentes na página de remoção de newsletter concluída.
    """
    assert_contains(resp_remocao_newsletter, "<title>McField's - Remoção concluída</title>")
    assert_contains(resp_remocao_newsletter, newsletter.title)


def test_remocao_newsletter(client_usuario_logado_com_perm_remocao, newsletter):
    """
    Certifica de que a newsletter foi removida com sucesso.
    """
    client_usuario_logado_com_perm_remocao.post(
        reverse('newsletter:remocao', args=(newsletter.id,)))
    if Newsletter.objects.exists():
        exists = True
    else:
        exists = False
    assert_false(exists)
