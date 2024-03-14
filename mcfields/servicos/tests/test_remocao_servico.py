import pytest
from django.urls import reverse
from mcfields.django_assertions import assert_contains, assert_false
from mcfields.servicos.models import Service


@pytest.fixture
def resp_remocao_servico(service, client_usuario_log_com_perm_remocao_serv):
    """
    Realiza uma requisição post na página de confirmação de remoção de serviço
    para concretizar a remoção.
    """
    resp = client_usuario_log_com_perm_remocao_serv.post(reverse('servicos:remocao', args=(service.pk,)))
    return resp


def test_pag_remocao_serv_concluida(resp_remocao_servico, service):
    """
    Certifica de que a página de confirmação de serviço foi carregada com sucesso.
    """
    assert resp_remocao_servico.status_code == 200
    assert resp_remocao_servico.wsgi_request.path == f'/servicos/adm/remocao/{service.pk}'


def test_titulo_serv_pag_remocao_concluida(resp_remocao_servico, service):
    """
    Certifica de que o título do serviço removido está presente na página de remoção concluída.
    """
    assert_contains(resp_remocao_servico, service.title)


def test_remocao_servico(resp_remocao_servico, service):
    """
    Certifica de que o serviço foi de fato removido do banco de dados.
    """
    assert_false(Service.objects.exists())
