import pytest
from django.urls import reverse


@pytest.fixture
def resp_indice_newsletters(client):
    """
    Cria uma requisição na página de índice de newsletters.
    """
    response = client.get(reverse('newsletter:indice_newsletters'))
    return response


def test_status_code_indice_newsletter(resp_indice_newsletters):
    """
    Certifica de que a página de índice de newsletters foi carregada com sucesso.
    """
    assert resp_indice_newsletters.status_code == 200
