import pytest
from django.urls import reverse


@pytest.fixture
def resp_post_news_success(client):
    """
    Realiza uma requisição na paǵina que informa que a newsletter foi postada com sucesso.
    """
    response = client.get(reverse('newsletter:post_success'))
    return response


def test_status_code_news_post_success(resp_post_news_success):
    """
    Certifica de que a página que informa a postagem da newsletter com sucesso foi carregada.
    """
    assert resp_post_news_success.status_code == 200
