import pytest
from django.urls import reverse
from model_bakery import baker
from datetime import date
from mcfields.django_assertions import assert_contains
from mcfields.newsletter.models import Newsletter


@pytest.fixture
def newsletters(db):
    """
    Cria algumas newsletters para serem apresentadas na página de índice. O campo 'content' foi preenchido por conta
    de ser um campo CKEditor5Field, que não é suportado pelo baker.
    :return: Newsletters criadas.
    """
    news = baker.make(Newsletter, _quantity=3, content='Texto da newsletter')
    return news


@pytest.fixture
def resp_indice_newsletters(client, newsletters):
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


def test_dados_newsletter_indice(resp_indice_newsletters, newsletters):
    """
    Certifica de que as informações de cada newsletter estão presentes na página de índice.
    """
    for newsletter in newsletters:
        pub_date = date.strftime(newsletter.pub_date, "%d/%m/%Y")
        assert_contains(resp_indice_newsletters, newsletter.title)
        assert_contains(resp_indice_newsletters, newsletter.intro)
        assert_contains(resp_indice_newsletters, newsletter.author)
        assert_contains(resp_indice_newsletters, pub_date)
