import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_contato(client):
    """
    Realiza uma requisição na página de contato.
    """
    resp = client.get(reverse('base:contato'))
    return resp


def test_status_code_pag_contato(resp_pag_contato):
    """
    Certifica de que a página de contato é carregada com sucesso.
    """
    assert resp_pag_contato.status_code == 200


def test_titulo_pag_contato(resp_pag_contato):
    """
    Certifica de que o título da página de contato está presente e correto.
    """
    assert_contains(resp_pag_contato, "<title>McField's - Contato</title>")


def test_form_contato(resp_pag_contato):
    """
    Certifica de que os campos do formulário de contato estão presentes.
    """
    assert_contains(resp_pag_contato, '<label for="id_name">Nome:</label>')
    assert_contains(resp_pag_contato, '<input type="text" name="name" maxlength="32" required id="id_name">')
    assert_contains(resp_pag_contato, '<label for="id_email">Email:</label>')
    assert_contains(resp_pag_contato, '<input type="email" name="email" maxlength="48" required id="id_email">')
    assert_contains(resp_pag_contato, '<label for="id_subject">Assunto:</label>')
    assert_contains(resp_pag_contato, '<input type="text" name="subject" maxlength="128" required id="id_subject">')
    assert_contains(resp_pag_contato, '<label for="id_message">Mensagem:</label>')
    assert_contains(resp_pag_contato, '<textarea name="message" cols="40" rows="10" '
                                      'required id="id_message">\n</textarea>')
    assert_contains(resp_pag_contato, '<input type="checkbox" name="agree_with_policy" id="id_agree_with_policy">')
    assert_contains(resp_pag_contato, f'Estou ciente e de acordo com a <a '
                                      f'href="{reverse("base:politica_privacidade")}">Política de Privacidade</a>')
    assert_contains(resp_pag_contato, f'<a class="canc-button" href="{reverse("base:home")}">Cancelar</a>')
    assert_contains(resp_pag_contato, '<button class="submit-button" type="submit">Enviar</button>')
