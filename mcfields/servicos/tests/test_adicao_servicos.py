import io
import pytest
from django.core.files.base import ContentFile
from django.urls import reverse
from model_bakery import baker
from mcfields.django_assertions import assert_true, assert_contains, assert_false
from mcfields.servicos.models import Servico
from PIL import Image


@pytest.fixture
def imagem(settings):
    """
    Cria uma imagem para ser usada na postagem de um novo serviço. A configuração STORAGES deve ser sobrescrita
    utilizando InMemoryStorage, caso contrário a imagem será persistida/salva na pasta mediafiles.
    """
    settings.STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.InMemoryStorage",
        }
    }
    stream = io.BytesIO()
    image = Image.new('RGB', (200, 200), color='white')
    image.save(stream, 'PNG')
    return ContentFile(stream.getvalue(), name='test.png')


@pytest.fixture
def servico(db):
    """
    Cria um serviço e salva no banco de dados.
    """
    servico = baker.make(Servico, content='Conteúdo serviço', slug='teste-slug-repetida')
    return servico


@pytest.fixture
def resp_post_serv_slug_repetida(client_usuario_log_com_perm_adic_serv, imagem):
    """
    Tenta realizar a postagem de um novo serviço com slug repetida.
    """
    resp = client_usuario_log_com_perm_adic_serv.post(reverse('servicos:adicionar'),
                                                      {'title': 'Título slug repetida',
                                                       'intro': 'Introdução slug repetida',
                                                       'home_picture': imagem,
                                                       'content': 'Conteúdo slug repetida',
                                                       'slug': 'teste-slug-repetida'})
    return resp


@pytest.fixture
def resp_adicao_novo_servico(client_usuario_log_com_perm_adic_serv, imagem):
    """
    Adiciona um novo serviço.
    """
    resp = client_usuario_log_com_perm_adic_serv.post(reverse('servicos:adicionar'),
                                                      {'title': 'Título do serviço',
                                                       'intro': 'Introdução do serviço',
                                                       'home_picture': imagem,
                                                       'content': 'Conteúdo do serviço',
                                                       'slug': 'titulo-do-servico'})
    return resp


def test_adicao_servico(resp_adicao_novo_servico):
    """
    Certifica de que o serviço foi de fato adicionado ao banco de dados.
    """
    saved_service = False
    if Servico.objects.get(slug='titulo-do-servico'):
        saved_service = True
    assert_true(saved_service)


def test_msg_servico_slug_repetida(servico, resp_post_serv_slug_repetida):
    """
    Certifica de que a mensagem de slug repetida é exibida para o usuário.
    """
    assert_contains(resp_post_serv_slug_repetida, 'Servico com este Slug já existe.')


def test_servico_slug_repetida_nao_salvo(servico, resp_post_serv_slug_repetida):
    """
    Certifica de que o serviço com slug repetida não foi salvo no banco de dados.
    """
    saved = False
    if Servico.objects.filter(title='Título slug repetida'):
        saved = True
    assert_false(saved)


def test_adic_servico_concluida(resp_adicao_novo_servico):
    """
    Certifica de que, após adicionar novo serviço, a página com a mensagem de adição com sucesso é renderizada.
    """
    assert_contains(resp_adicao_novo_servico, "<title>McField's - Publicação concluída</title>")
    assert_contains(resp_adicao_novo_servico, 'O serviço "<strong>Título do serviço</strong>" '
                                              'foi adicionado com sucesso.')
