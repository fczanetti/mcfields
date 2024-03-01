import pytest
from django.urls import reverse
from datetime import date
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_detalhe_newsletter(client, newsletter):
    """
    Cria uma requisição na página de detalhes da newsletter.
    """
    response = client.get(reverse('newsletter:detalhe_newsletter', args=(newsletter.slug,)))
    return response


def test_status_code_detalhe_newsletter(resp_detalhe_newsletter):
    """
    Certifica de que a página de detalhes da newsletter foi carregada com sucesso.
    """
    assert resp_detalhe_newsletter.status_code == 200


def test_newsletter_dados(resp_detalhe_newsletter, newsletter):
    """
    Certifica de que os dados da newsletter estão presentes na página de detalhe desta.
    """
    pub_date = date.strftime(newsletter.pub_date, '%d/%m/%Y')
    assert_contains(resp_detalhe_newsletter, f'<h1 id="newsletter-title">{newsletter.title}</h1>')
    assert_contains(resp_detalhe_newsletter, newsletter.intro)
    assert_contains(resp_detalhe_newsletter, newsletter.content)
    assert_contains(resp_detalhe_newsletter, f'<div id="news-pub-date">{pub_date}</div>')
    assert_contains(resp_detalhe_newsletter, f'<div id="newsletter-author">{newsletter.author}</div>')
