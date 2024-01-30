import pytest
from django.urls import reverse


@pytest.fixture
def resp(client):
    """
    Cria uma requisição na home page.
    """
    return client.get(reverse('base:home'))


def test_status_code_home(resp):
    """
    Certifica de que a home page foi carregada com sucesso.
    """
    assert resp.status_code == 200
