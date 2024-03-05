import pytest
from django.urls import reverse

from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_adic_servico_usuario_logado_com_perm(client_usuario_log_com_perm_adic_serv):
    """
    Realiza uma requisição na página de adicionar serviços com usuário não logado.
    """
    resp = client_usuario_log_com_perm_adic_serv.get(reverse('servicos:adicionar'))
    return resp


def test_status_code_pag_adic_serv_usuario_nao_logado(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que, ao tentar acessar a página de adição de serviços com usuário
    logado e com permissão a página carrega normalmente.
    """
    assert resp_pag_adic_servico_usuario_logado_com_perm.status_code == 200


def test_title_pag_adic_servicos(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que o título da página de adição de serviços está presente e correto.
    """
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm,
                    "<title>McField's - Adicionar serviço</title>")


def test_form_adic_serv(resp_pag_adic_servico_usuario_logado_com_perm):
    """
    Certifica de que os campos do formulário de adição de serviços estão presentes.
    """
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_title">Título:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<input type="text" name="title" maxlength="64" '
                                                                   'required id="id_title">')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_intro">Introdução:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<textarea name="intro" cols="40" rows="10" '
                                                                   'maxlength="512" required '
                                                                   'id="id_intro">\n</textarea>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_home_picture">Foto da home '
                                                                   'page:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<input type="file" name="home_picture" '
                                                                   'accept="image/*" required id="id_home_picture">')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_content">Conteúdo:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<div class="ck-editor-container">')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<label for="id_slug">Slug:</label>')
    assert_contains(resp_pag_adic_servico_usuario_logado_com_perm, '<input type="text" name="slug" maxlength="64" '
                                                                   'required id="id_slug">')
