import pytest
from django.urls import reverse
from model_bakery import baker
from mcfields.base.models import Subject
from mcfields.django_assertions import assert_true, assert_contains, assert_false


@pytest.fixture
def resp_adic_subject(client_usuario_logado_com_perm_adic_subject):
    """
    Realiza a adição de um novo assunto (subject).
    """
    resp = client_usuario_logado_com_perm_adic_subject.post(reverse('base:adic_subject'),
                                                            {'title': 'Título do assunto',
                                                             'description': 'Descrição',
                                                             'slug': 'titulo-do-assunto'})
    return resp


@pytest.fixture
def resp_adic_subject_slug_repetida(client_usuario_logado_com_perm_adic_subject):
    """
    Realiza a tentativa de adição de um novo assunto (subject) com slug repetida.
    """
    baker.make(Subject, slug='slug-repetida')
    resp = client_usuario_logado_com_perm_adic_subject.post(reverse('base:adic_subject'),
                                                            {'title': 'Slug repetida',
                                                             'description': 'Descrição',
                                                             'slug': 'slug-repetida'})
    return resp


def test_subject_adicionado(resp_adic_subject):
    """
    Certifica de que o assunto foi adicionado/salvo no banco de dados.
    """
    assert_true(Subject.objects.filter(title='Título do assunto').exists())


def test_titulo_assunto_pag_adicao_concluida(resp_adic_subject):
    """
    Certifica de que o título do assunto está presente na página de
    adição concluída.
    """
    assert_contains(resp_adic_subject, 'Título do assunto')


def test_titulo_pag_adic_subject_concluida(resp_adic_subject):
    """
    Certifica de que o título da página de adição de assunto concluída
    está presente e correto.
    """
    assert_contains(resp_adic_subject, "<title>McField's - Adição concluída</title>")


def test_subject_slug_repetida_nao_adicionado(resp_adic_subject_slug_repetida):
    """
    Certifca de que o subject com slug repetida não foi adicionado ao banco de dados.
    """
    assert_false(Subject.objects.filter(title='Slug repetida').exists())
