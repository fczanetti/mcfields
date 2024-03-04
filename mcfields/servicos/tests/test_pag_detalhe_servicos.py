import pytest
from django.urls import reverse
from model_bakery import baker

from mcfields.django_assertions import assert_contains
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
