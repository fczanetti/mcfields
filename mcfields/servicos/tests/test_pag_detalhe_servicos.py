import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.django_assertions import assert_contains, assert_not_contains
from mcfields.servicos.models import Service


@pytest.fixture
def service(db):
    """
    Cria um serviço e retorna este.
    """
    servico = baker.make(Service, content='Detalhes do serviço')
    return servico


@pytest.fixture
def resp_pagina_detalhe_servico(client, service):
    """
    Cria uma requisição na página de detalhes de serviços com usuário não logado.
    """
    resp = client.get(reverse('servicos:detalhe_servico', args=(service.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_servico_usuario_logado_sem_perm(client_usuario_logado, service):
    """
    Cria uma requisição na página de detalhes de serviços
    com usuário logado e sem permissão de adição nem edição.
    """
    resp = client_usuario_logado.get(reverse('servicos:detalhe_servico', args=(service.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_serv_usuario_log_com_perm_adic(client_usuario_log_com_perm_adic_serv, service):
    """
    Cria uma requisição na página de detalhes de serviços com
    usuário logado e com permissão de adição.
    """
    resp = client_usuario_log_com_perm_adic_serv.get(reverse('servicos:detalhe_servico', args=(service.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_serv_usuario_log_com_perm_edic(client_usuario_log_com_perm_edic_serv, service):
    """
    Cria uma requisição na página de detalhes de serviços com
    usuário logado e com permissão de edição.
    """
    resp = client_usuario_log_com_perm_edic_serv.get(reverse('servicos:detalhe_servico', args=(service.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_serv_usuario_log_com_perm_remocao_serv(client_usuario_log_com_perm_remocao_serv, service):
    """
    Cria uma requisição na página de detalhes de serviço com usuário
    logado e com permissão de remoção de serviço.
    """
    resp = client_usuario_log_com_perm_remocao_serv.get(
        reverse('servicos:detalhe_servico', args=(service.slug,)))
    return resp


def test_status_code_detalhe_servico(resp_pagina_detalhe_servico):
    """
    Certifica de que a página de detalhes de serviço carrega com sucesso.
    """
    assert resp_pagina_detalhe_servico.status_code == 200


def test_titulo_pag_detalhe_servico(resp_pagina_detalhe_servico, service):
    """
    Certifica de que o título da página de detalhes do serviço está presente e correto.
    """
    assert_contains(resp_pagina_detalhe_servico, f"<title>McField's - {service.title}</title>")


def test_infos_pag_detalhe_servico(resp_pagina_detalhe_servico, service):
    """
    Certifica de que as informações do serviço estão presentes na página de detalhes deste.
    """
    assert_contains(resp_pagina_detalhe_servico, f'<h1 id="service-title">{service.title}</h1>')
    assert_contains(resp_pagina_detalhe_servico, service.content)


def test_botao_edicao_e_adicao_servico_usuario_nao_logado(resp_pagina_detalhe_servico, service):
    """
    Certifica de que os botões de edição e adição de serviço não estão presentes.
    """
    assert_not_contains(resp_pagina_detalhe_servico, f'<a id="service-update-link" '
                                                     f'href="{service.get_edition_url()}">Editar</a>')
    assert_not_contains(resp_pagina_detalhe_servico, f'<a id="service-adit-link" '
                                                     f'href="{reverse("servicos:adicionar")}">Novo serviço</a>')


def test_botao_edic_e_adic_serv_usuario_log_sem_perm(resp_pag_det_servico_usuario_logado_sem_perm, service):
    """
    Certifica de que os botões de edição e adição de serviço não estão presentes.
    """
    assert_not_contains(resp_pag_det_servico_usuario_logado_sem_perm, f'<a id="service-update-link" '
                                                                      f'href="{service.get_edition_url()}">Editar</a>')
    assert_not_contains(resp_pag_det_servico_usuario_logado_sem_perm, f'<a id="service-adit-link" '
                                                                      f'href="{reverse("servicos:adicionar")}">'
                                                                      f'Novo serviço</a>')


def test_botao_adic_usuario_logado_com_perm_adic(resp_pag_det_serv_usuario_log_com_perm_adic):
    """
    Certifica de que o botão de adição de serviço está presente
    para o usuário logado com permissão.
    """
    assert_contains(resp_pag_det_serv_usuario_log_com_perm_adic, f'<a id="service-adit-link" '
                                                                 f'href="{reverse("servicos:adicionar")}">'
                                                                 f'Novo serviço</a>')


def test_botao_edic_usuario_logado_com_perm_edic(resp_pag_det_serv_usuario_log_com_perm_edic, service):
    """
    Certifica de que o botão de edição de serviço está presente
    para o usuário logado com permissão.
    """
    assert_contains(resp_pag_det_serv_usuario_log_com_perm_edic, f'<a id="service-update-link" '
                                                                 f'href="{service.get_edition_url()}">Editar</a>')


def test_botao_remocao_indisp_usuario_nao_logado(resp_pagina_detalhe_servico):
    """
    Certifica de que o botão de remoção de serviço não está disponível
    na página de detalhes para o usuário que não está logado.
    """
    assert_not_contains(resp_pagina_detalhe_servico, 'Remover')


def test_botao_remoc_indisp_usuario_log_sem_perm_remoc_serv(resp_pag_det_servico_usuario_logado_sem_perm):
    """
    Certifica de que o botão de remoção de serviço não está disponível
    para o usuário logado sem permissão de remoção.
    """
    assert_not_contains(resp_pag_det_servico_usuario_logado_sem_perm, 'Remover')


def test_botao_remoc_disp_usuario_log_com_perm_remoc_serv(resp_pag_det_serv_usuario_log_com_perm_remocao_serv):
    """
    Certifica de que o botão de remoção de serviço está disponível
    para o usuário logado e com permissão de remoção.
    """
    assert_contains(resp_pag_det_serv_usuario_log_com_perm_remocao_serv, 'Remover')
