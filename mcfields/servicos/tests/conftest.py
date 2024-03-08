import io
from django.core.files.base import ContentFile
from PIL import Image
import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from mcfields.servicos.models import Servico
from model_bakery import baker


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
    Cria e retorna um serviço.
    """
    serv = baker.make(Servico, content='Conteúdo do serviço teste')
    return serv


@pytest.fixture
def usuario_senha_plana_com_perm_edic_serv(usuario_senha_plana):
    """
    Cria um usuário com permissão de edição de serviços.
    """
    content_type = ContentType.objects.get_for_model(Servico)
    permission = Permission.objects.get(codename='change_servico', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_edicao = usuario_senha_plana
    return usuario_com_perm_edicao


@pytest.fixture
def client_usuario_log_com_perm_edic_serv(usuario_senha_plana_com_perm_edic_serv, client):
    """
    Cria um client com usuário logado e permissão de edição de serviços.
    """
    client.force_login(usuario_senha_plana_com_perm_edic_serv)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_remocao_serv(usuario_senha_plana):
    """
    Cria um usuário com permissão de remoção de serviços.
    """
    content_type = ContentType.objects.get_for_model(Servico)
    permission = Permission.objects.get(codename='delete_servico', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_remoca = usuario_senha_plana
    return usuario_com_perm_remoca


@pytest.fixture
def client_usuario_log_com_perm_remocao_serv(client, usuario_senha_plana_com_perm_remocao_serv):
    """
    Cria um cliente com usuário logado e permissão de remoção de serviços.
    """
    client.force_login(usuario_senha_plana_com_perm_remocao_serv)
    return client
