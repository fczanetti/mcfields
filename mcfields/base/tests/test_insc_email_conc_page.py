import pytest
from django.urls import reverse


@pytest.fixture
def resp_inscricao_email_concluida(client):
    """
    Realiza uma requisição na página de inscrição de email concluída.
    """
    resp = client.get(reverse('base:inscricao_concluida'))
    return resp


def test_status_code_insc_email_conc(resp_inscricao_email_concluida):
    """
    Certifica de que a página de inscrição de email concluída foi carregada com sucesso.
    """
    assert resp_inscricao_email_concluida.status_code == 200
