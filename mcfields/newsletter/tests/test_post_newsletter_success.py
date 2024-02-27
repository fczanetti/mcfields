import pytest
# from django.urls import reverse


@pytest.fixture
def resp_post_news_success(client):
    """
    Realiza a postagem de uma nova newsletter.
    """
