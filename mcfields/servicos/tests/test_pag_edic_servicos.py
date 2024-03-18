import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_edicao_serv_usuario_nao_logado(client, service):
    """
    Realiza uma requisição na página de edição de serviços com usuário não logado.
    """
    resp = client.get(reverse('servicos:edicao', args=(service.pk,)))
    return resp


@pytest.fixture
def resp_pag_edicao_serv_usuario_logado_sem_perm(client_usuario_logado, service):
    """
    Realiza uma requisição na página de edição de serviços com usuário
    logado e sem permissão de edição.
    """
    resp = client_usuario_logado.get(reverse('servicos:edicao', args=(service.pk,)))
    return resp


@pytest.fixture
def resp_pag_edicao_serv_usuario_logado_com_perm(client_usuario_log_com_perm_edic_serv, service):
    """
    Realiza uma requisição na página de edição de serviços com
    usuário logado e com permissão de edição.
    """
    resp = client_usuario_log_com_perm_edic_serv.get(reverse('servicos:edicao', args=(service.pk,)))
    return resp


def test_pag_edicao_serv_usuario_nao_logado(resp_pag_edicao_serv_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de edição de serviços com usuário
    não logado o mesmo é redirecionado para a página de login.
    """
    assert resp_pag_edicao_serv_usuario_nao_logado.status_code == 302
    assert resp_pag_edicao_serv_usuario_nao_logado.url.startswith('/accounts/login/')


def test_pag_edicao_serv_usuario_logado_sem_perm(resp_pag_edicao_serv_usuario_logado_sem_perm):
    """
    Certifica de que, ao tentar acessar a página de edição de serviços com usuário
    logado sem permissão de edição, o mesmo é redirecionado para a página de acesso não permitido.
    """
    assert resp_pag_edicao_serv_usuario_logado_sem_perm.status_code == 302
    assert resp_pag_edicao_serv_usuario_logado_sem_perm.url.startswith('/nao_permitido/')


def test_pag_edicao_serv_usuario_logado_com_perm(resp_pag_edicao_serv_usuario_logado_com_perm):
    """
    Certifica de que, ao tentar acessar a página de edição de serviços com usuário
    logado e com permissão de edição, esta é carregada com sucesso.
    """
    assert resp_pag_edicao_serv_usuario_logado_com_perm.status_code == 200


def test_titulo_pag_edicao_serv(resp_pag_edicao_serv_usuario_logado_com_perm):
    """
    Certifica de que o título da página de edição de serviço está presente e correto.
    """
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, "<title>McField's - Edição de Serviço</title>")


def test_infos_servico_pag_edicao(resp_pag_edicao_serv_usuario_logado_com_perm, service):
    """
    Certifica de que as informações do serviço a ser editado estão presentes
    na página de edição.
    """
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, f'<input type="text" name="title" '
                                                                  f'value="{service.title}" maxlength="64" '
                                                                  f'required id="id_title">')
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, service.intro)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, service.home_picture)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, service.content)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, service.slug)


def test_direcionamento_botao_cancelar(resp_pag_edicao_serv_usuario_logado_com_perm, service):
    """
    Certifica de que o botão cancelar, no momento da edição de um serviço, tem a função
    de direcionar o usuário para a página de detalhes do serviço que estava editando.
    """
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm,
                    f'<a class="canc-button" '
                    f'href="{reverse("servicos:detalhe_servico", args=(service.slug,))}">Cancelar</a>')


def test_titulo_form(resp_pag_edicao_serv_usuario_logado_com_perm, service):
    """
    Certifica de que o título do formulário está presente e
    indicando a edição de um serviço existente.
    """
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, f'<h1 class="form-title">Edição do Serviço '
                                                                  f'"{service.title}"</h1>')
