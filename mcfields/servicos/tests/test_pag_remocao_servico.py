import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_confirm_remocao_serv_usuario_nao_logado(client, servico):
    """
    Cria uma requisição na página de remoção de serviço com um
    usuário não logado.
    """
    resp = client.get(reverse('servicos:remocao', args=(servico.pk,)))
    return resp


@pytest.fixture
def resp_conf_remoc_serv_usuario_log_sem_perm_remocao(client_usuario_logado, servico):
    """
    Cria uma requisição na página de remoção de serviço com um
    usuário logado sem permissão de remoção.
    """
    resp = client_usuario_logado.get(reverse('servicos:remocao', args=(servico.pk,)))
    return resp


@pytest.fixture
def resp_conf_remoc_serv_usuario_log_com_perm_remocao(client_usuario_log_com_perm_remocao_serv, servico):
    """
    Cria uma requisição na página de confirmação de remoção de serviços
    com usuário logado e com permissão de remoção.
    """
    resp = client_usuario_log_com_perm_remocao_serv.get(reverse('servicos:remocao', args=(servico.pk,)))
    return resp


def test_redirect_usuario_nao_logado(resp_confirm_remocao_serv_usuario_nao_logado):
    """
    Certifica de que, ao tentar acessar a página de remoção de serviços com usuário
    não logado, o mesmo é redirecionado para a página de login.
    """
    assert resp_confirm_remocao_serv_usuario_nao_logado.status_code == 302
    assert resp_confirm_remocao_serv_usuario_nao_logado.url.startswith('/accounts/login/')


def test_redirect_usuario_log_sem_perm_remoc_serv(resp_conf_remoc_serv_usuario_log_sem_perm_remocao):
    """
    Certifica de que, ao tentar acessar a página de confirmação de remoção de serviços
    com usuário logado sem permissão, o mesmo é direcionado para a página de acesso negado.
    """
    assert resp_conf_remoc_serv_usuario_log_sem_perm_remocao.status_code == 302
    assert resp_conf_remoc_serv_usuario_log_sem_perm_remocao.url.startswith('/nao_permitido/')


def test_status_code_pag_conf_remocao_servicos(resp_conf_remoc_serv_usuario_log_com_perm_remocao):
    """
    Certifica de que, ao tentar acessar a página de confirmação de remoção de serviços
    com usuário logado e com permissão, a página é carregada com sucesso.
    """
    assert resp_conf_remoc_serv_usuario_log_com_perm_remocao.status_code == 200


def test_titulo_pag_confirm_remocao(resp_conf_remoc_serv_usuario_log_com_perm_remocao):
    """
    Certifica de que o título da página de confirmação de remoção de serviços
    está presente e correto.
    """
    assert_contains(resp_conf_remoc_serv_usuario_log_com_perm_remocao, "<title>McField's - Confirmar remoção</title>")


def test_titulo_serv_pag_conf_remocao(resp_conf_remoc_serv_usuario_log_com_perm_remocao, servico):
    """
    Certifica de que o título do serviço a ser removido está presente na página
    de confirmação de remoção deste.
    """
    assert_contains(resp_conf_remoc_serv_usuario_log_com_perm_remocao, servico.title)


def test_botao_cancelar_pag_conf_remocao_serv(resp_conf_remoc_serv_usuario_log_com_perm_remocao, servico):
    """
    Certifica de que o botão de cancelar remoção está presente e direcionando para
    a página de detalhes do serviço que será removido.
    """
    assert_contains(resp_conf_remoc_serv_usuario_log_com_perm_remocao,
                    f'<a id="canc-removal-button" href="{servico.get_absolute_url()}">Cancelar</a>')


def test_action_form_remocao_servico(resp_conf_remoc_serv_usuario_log_com_perm_remocao, servico):
    """
    Certifica de que a action do formulário de remoção do serviço está direcionando a submissão
    para a própria página de remoção.
    """
    assert_contains(resp_conf_remoc_serv_usuario_log_com_perm_remocao,
                    f'<form action="{reverse("servicos:remocao", args=(servico.pk,))}" method="POST">')
