import pytest
from django.urls import reverse


@pytest.fixture
def resp_sobre(client):
    """
    Cria uma requisição na página "sobre".
    """
    response = client.get(reverse('base:sobre'))
    return response


def test_status_code_sobre(resp_sobre):
    """
    Certifica de que a página "sobre" é carregada com sucesso.
    """
    assert resp_sobre.status_code == 200
