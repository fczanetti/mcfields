import pytest
from django.urls import reverse
from model_bakery import baker
from datetime import date
from mcfields.django_assertions import assert_contains, assert_not_contains
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


# @pytest.fixture
# def unordered_newsletters(db):
#     """
#     Cria algumas newsletters não ordenadas.
#     """
#     news = [baker.make(Newsletter, content='Newsletter não ordenada', pub_date=pub_date)
#             for pub_date in ['2024-03-01', '2024-03-05', '2024-02-22', '2024-03-02']]
#     return news


@pytest.fixture
def resp_indice_newsletters(client, newsletters):
    """
    Cria uma requisição na página de índice de newsletters.
    """
    response = client.get(reverse('newsletter:indice_newsletters'))
    return response


@pytest.fixture
def resp_indice_newsletters_usuario_logado(client_usuario_logado):
    """
    Cria uma requisição na página de índice de newsletters com usuário logado.
    """
    response = client_usuario_logado.get(reverse('newsletter:indice_newsletters'))
    return response


def test_status_code_indice_newsletter(resp_indice_newsletters):
    """
    Certifica de que a página de índice de newsletters foi carregada com sucesso.
    """
    assert resp_indice_newsletters.status_code == 200


def test_titulo_pag_indice_newsletter(resp_indice_newsletters):
    """
    Certifica de que o título da página de índice de newsletters está presente e correto.
    """
    assert_contains(resp_indice_newsletters, "<title>McField's - Newsletter</title>")


def test_dados_newsletter_indice(resp_indice_newsletters, newsletters):
    """
    Certifica de que as informações de cada newsletter estão presentes na página de índice.
    """
    for newsletter in newsletters:
        pub_date = date.strftime(newsletter.pub_date, "%d/%m/%Y")
        assert_contains(resp_indice_newsletters, f'<h4 class="newsletter-title">{newsletter.title}</h4>')
        assert_contains(resp_indice_newsletters, f'<p class="newsletter-comment">{newsletter.intro}</p>')
        assert_contains(resp_indice_newsletters, f'<div class="newsletter-author">{newsletter.author}</div>')
        assert_contains(resp_indice_newsletters, f'<div class="newsletter-date">{pub_date}</div>')
        assert_contains(resp_indice_newsletters, f'<a href="{newsletter.get_absolute_url()}" '
                                                 f'class="newsletter-box-link">')


def test_botao_nova_news_disponivel(client_usuario_logado_com_perm_postagem):
    """
    Certifica de que, com o usuário logado e tendo permissão de postar, o botão de nova newsletter é exibido.
    """
    response = client_usuario_logado_com_perm_postagem.get(reverse('newsletter:indice_newsletters'))
    assert_contains(response, f'<a id="new-pub-link" href="{reverse("newsletter:post")}">Nova publicação</a>')


def test_botao_nova_news_indisponivel(resp_indice_newsletters_usuario_logado):
    """
    Certifica de que, mesmo com o usuário logado, o botão de nova
    newsletter não é exibido se o usuário não tem permissão.
    """
    assert_not_contains(resp_indice_newsletters_usuario_logado, 'Nova publicação')


# def test_list_ordered_newsletters(unordered_newsletters):
#     """
#     Certifica de que as newsletters estão sendo ordenadas por data de publicação (reversamente).
#     """
#     ordered_news = facade.listar_newsletters_ordenadas()
#     ordered_news_2 = list(sorted(unordered_newsletters, key=lambda news: news.pub_date, reverse=True))
#     assert (ordered_news == ordered_news_2)
