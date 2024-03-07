import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.django_assertions import assert_contains, assert_not_contains
from mcfields.servicos.models import Servico


@pytest.fixture
def servico(db):
    """
    Cria um serviço e retorna este.
    """
    servico = baker.make(Servico, content='Detalhes do serviço')
    return servico


@pytest.fixture
def resp_pagina_detalhe_servico(client, servico):
    """
    Cria uma requisição na página de detalhes de serviços com usuário não logado.
    """
    resp = client.get(reverse('servicos:detalhe_servico', args=(servico.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_servico_usuario_logado_sem_perm(client_usuario_logado, servico):
    """
    Cria uma requisição na página de detalhes de serviços
    com usuário logado e sem permissão de adição nem edição.
    """
    resp = client_usuario_logado.get(reverse('servicos:detalhe_servico', args=(servico.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_serv_usuario_log_com_perm_adic(client_usuario_log_com_perm_adic_serv, servico):
    """
    Cria uma requisição na página de detalhes de serviços com
    usuário logado e com permissão de adição.
    """
    resp = client_usuario_log_com_perm_adic_serv.get(reverse('servicos:detalhe_servico', args=(servico.slug,)))
    return resp


@pytest.fixture
def resp_pag_det_serv_usuario_log_com_perm_edic(client_usuario_log_com_perm_edic_serv, servico):
    """
    Cria uma requisição na página de detalhes de serviços com
    usuário logado e com permissão de edição.
    """
    resp = client_usuario_log_com_perm_edic_serv.get(reverse('servicos:detalhe_servico', args=(servico.slug,)))
    return resp


def test_status_code_detalhe_servico(resp_pagina_detalhe_servico):
    """
    Certifica de que a página de detalhes de serviço carrega com sucesso.
    """
    assert resp_pagina_detalhe_servico.status_code == 200


def test_titulo_pag_detalhe_servico(resp_pagina_detalhe_servico, servico):
    """
    Certifica de que o título da página de detalhes do serviço está presente e correto.
    """
    assert_contains(resp_pagina_detalhe_servico, f"<title>McField's - {servico.title}</title>")


def test_infos_pag_detalhe_servico(resp_pagina_detalhe_servico, servico):
    """
    Certifica de que as informações do serviço estão presentes na página de detalhes deste.
    """
    assert_contains(resp_pagina_detalhe_servico, f'<h1 id="service-title">{servico.title}</h1>')
    assert_contains(resp_pagina_detalhe_servico, servico.content)


def test_botao_edicao_e_adicao_servico_usuario_nao_logado(resp_pagina_detalhe_servico, servico):
    """
    Certifica de que os botões de edição e adição de serviço não estão presentes.
    """
    assert_not_contains(resp_pagina_detalhe_servico, f'<a id="service-update-link" '
                                                     f'href="{servico.get_edition_url()}">Editar</a>')
    assert_not_contains(resp_pagina_detalhe_servico, f'<a id="service-adit-link" '
                                                     f'href="{reverse("servicos:adicionar")}">Novo serviço</a>')


def test_botao_edic_e_adic_serv_usuario_log_sem_perm(resp_pag_det_servico_usuario_logado_sem_perm, servico):
    """
    Certifica de que os botões de edição e adição de serviço não estão presentes.
    """
    assert_not_contains(resp_pag_det_servico_usuario_logado_sem_perm, f'<a id="service-update-link" '
                                                                      f'href="{servico.get_edition_url()}">Editar</a>')
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


def test_botao_edic_usuario_logado_com_perm_edic(resp_pag_det_serv_usuario_log_com_perm_edic, servico):
    """
    Certifica de que o botão de edição de serviço está presente
    para o usuário logado com permissão.
    """
    assert_contains(resp_pag_det_serv_usuario_log_com_perm_edic, f'<a id="service-update-link" '
                                                                 f'href="{servico.get_edition_url()}">Editar</a>')
