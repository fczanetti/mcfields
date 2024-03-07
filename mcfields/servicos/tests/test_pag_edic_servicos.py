import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_pag_edicao_serv_usuario_nao_logado(client, servico):
    """
    Realiza uma requisição na página de edição de serviços com usuário não logado.
    """
    resp = client.get(reverse('servicos:edicao', args=(servico.pk,)))
    return resp


@pytest.fixture
def resp_pag_edicao_serv_usuario_logado_sem_perm(client_usuario_logado, servico):
    """
    Realiza uma requisição na página de edição de serviços com usuário
    logado e sem permissão de edição.
    """
    resp = client_usuario_logado.get(reverse('servicos:edicao', args=(servico.pk,)))
    return resp


@pytest.fixture
def resp_pag_edicao_serv_usuario_logado_com_perm(client_usuario_log_com_perm_edic_serv, servico):
    """
    Realiza uma requisição na página de edição de serviços com
    usuário logado e com permissão de edição.
    """
    resp = client_usuario_log_com_perm_edic_serv.get(reverse('servicos:edicao', args=(servico.pk,)))
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
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, "<title>McField's - Edição de serviço</title>")


def test_infos_servico_pag_edicao(resp_pag_edicao_serv_usuario_logado_com_perm, servico):
    """
    Certifica de que as informações do serviço a ser editado estão presentes
    na página de edição.
    """
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, servico.title)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, servico.intro)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, servico.home_picture)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, servico.content)
    assert_contains(resp_pag_edicao_serv_usuario_logado_com_perm, servico.slug)
