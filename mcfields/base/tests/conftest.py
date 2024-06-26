import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from model_bakery import baker

from mcfields.base.models import Subject, Contact


@pytest.fixture
def usuario_senha_plana_com_perm_adic_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de adição de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='add_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_adic_subject = usuario_senha_plana
    return usuario_com_perm_adic_subject


@pytest.fixture
def client_usuario_logado_com_perm_adic_subject(client, usuario_senha_plana_com_perm_adic_subject):
    """
    Cria um cliente com usuário logado e com permissão de adição de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_adic_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_edic_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de edição de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='change_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_edic_subject = usuario_senha_plana
    return usuario_com_perm_edic_subject


@pytest.fixture
def client_usuario_logado_com_perm_edic_subject(client, usuario_senha_plana_com_perm_edic_subject):
    """
    Cria um cliente com usuário logado e com permissão de edição de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_edic_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de visualização de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='view_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_view_subject = usuario_senha_plana
    return usuario_com_perm_view_subject


@pytest.fixture
def client_usuario_logado_com_perm_view_subject(client, usuario_senha_plana_com_perm_view_subject):
    """
    Cria um cliente com usuário logado e com permissão de visualização de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_view_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_e_adic_subject(usuario_senha_plana_com_perm_view_subject):
    """
    Cria um usuário com permissão de visualização e adição de subjects
    (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='add_subject', content_type=content_type)
    usuario_senha_plana_com_perm_view_subject.user_permissions.add(permission)
    usuario_com_perm_view_e_add_subject = usuario_senha_plana_com_perm_view_subject
    return usuario_com_perm_view_e_add_subject


@pytest.fixture
def client_usuario_logado_com_perm_view_e_add_subject(client, usuario_senha_plana_com_perm_view_e_adic_subject):
    """
    Cria um cliente com usuário logado e com permissão de visualização e adição de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_view_e_adic_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_remoc_subject(usuario_senha_plana):
    """
    Cria um usuário com permissão de remoção de subjects (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='delete_subject', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_remoc_subject = usuario_senha_plana
    return usuario_com_perm_remoc_subject


@pytest.fixture
def client_usuario_logado_com_perm_remoc_subject(client, usuario_senha_plana_com_perm_remoc_subject):
    """
    Cria um cliente com usuário logado e com permissão de remoção de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_remoc_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_e_edic_subject(usuario_senha_plana_com_perm_view_subject):
    """
    Cria um usuário com permissão de visualização e edição de subjects
    (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='change_subject', content_type=content_type)
    usuario_senha_plana_com_perm_view_subject.user_permissions.add(permission)
    usuario_com_perm_view_e_edic_subject = usuario_senha_plana_com_perm_view_subject
    return usuario_com_perm_view_e_edic_subject


@pytest.fixture
def client_usuario_logado_com_perm_view_e_edic_subject(client, usuario_senha_plana_com_perm_view_e_edic_subject):
    """
    Cria um cliente com usuário logado e com permissão de visualização e edição de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_view_e_edic_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_e_remoc_subject(usuario_senha_plana_com_perm_view_subject):
    """
    Cria um usuário com permissão de visualização e remoção de subjects
    (assuntos) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Subject)
    permission = Permission.objects.get(codename='delete_subject', content_type=content_type)
    usuario_senha_plana_com_perm_view_subject.user_permissions.add(permission)
    usuario_com_perm_view_e_remoc_subject = usuario_senha_plana_com_perm_view_subject
    return usuario_com_perm_view_e_remoc_subject


@pytest.fixture
def client_usuario_logado_com_perm_view_e_remoc_subject(client, usuario_senha_plana_com_perm_view_e_remoc_subject):
    """
    Cria um cliente com usuário logado e com permissão de visualização e remoção de subjects (assuntos).
    """
    client.force_login(usuario_senha_plana_com_perm_view_e_remoc_subject)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_contact(usuario_senha_plana):
    """
    Cria um usuário com permissão de visualização de mensagens (contacts) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Contact)
    permission = Permission.objects.get(codename='view_contact', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_view_contact = usuario_senha_plana
    return usuario_com_perm_view_contact


@pytest.fixture
def client_usuario_logado_com_perm_view_contact(client, usuario_senha_plana_com_perm_view_contact):
    """
    Cria um cliente com usuário logado e com permissão de visualização de mensagens (contacts).
    """
    client.force_login(usuario_senha_plana_com_perm_view_contact)
    return client


@pytest.fixture
def mensagem(db):
    """
    Cria e retorna uma mensagem.
    """
    msg = baker.make(Contact)
    return msg


@pytest.fixture
def usuario_senha_plana_com_perm_remoc_contact(usuario_senha_plana):
    """
    Cria um usuário com permissão de remoção de mensagens (contacts) a partir do usuário_senha_plana.
    """
    content_type = ContentType.objects.get_for_model(Contact)
    permission = Permission.objects.get(codename='delete_contact', content_type=content_type)
    usuario_senha_plana.user_permissions.add(permission)
    usuario_com_perm_remocao_contact = usuario_senha_plana
    return usuario_com_perm_remocao_contact


@pytest.fixture
def client_usuario_logado_com_perm_remoc_contact(client, usuario_senha_plana_com_perm_remoc_contact):
    """
    Cria um cliente com usuário logado e com permissão de remoção de mensagens (contacts).
    """
    client.force_login(usuario_senha_plana_com_perm_remoc_contact)
    return client


@pytest.fixture
def usuario_senha_plana_com_perm_view_e_remoc_contact(usuario_senha_plana_com_perm_remoc_contact):
    """
    Cria um usuário com permissão de visualização e remoção de
    mensagens (contacts) a partir do usuário com permissão de remoção.
    """
    content_type = ContentType.objects.get_for_model(Contact)
    permission = Permission.objects.get(codename='view_contact', content_type=content_type)
    usuario_senha_plana_com_perm_remoc_contact.user_permissions.add(permission)
    usuario_com_perm_view_e_remocao_contact = usuario_senha_plana_com_perm_remoc_contact
    return usuario_com_perm_view_e_remocao_contact


@pytest.fixture
def client_usuario_logado_com_perm_view_e_remoc_contact(client, usuario_senha_plana_com_perm_view_e_remoc_contact):
    """
    Cria um cliente com usuário logado e com permissão de visualização e remoção de mensagens (contacts).
    """
    client.force_login(usuario_senha_plana_com_perm_view_e_remoc_contact)
    return client
