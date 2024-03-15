import pytest
from django.urls import reverse
from mcfields.base.models import Subject
from mcfields.django_assertions import assert_contains


@pytest.fixture
def resp_edicao_subject(client_usuario_logado_com_perm_edic_subject, subject):
    """
    Realiza uma edição em um subject já criado.
    """
    resp = client_usuario_logado_com_perm_edic_subject.post(reverse('base:edic_subject', args=(subject.pk,)),
                                                            {'title': 'Título alterado',
                                                             'description': 'Descrição alterada',
                                                             'slug': 'slug-alterada'})
    return resp


def test_edicao_infos_subject(resp_edicao_subject, subject):
    """
    Certifica de que o objeto foi editado com sucessp.
    """
    subject_alterado = Subject.objects.get(id=subject.pk)
    assert subject_alterado.title == 'Título alterado'
    assert subject_alterado.description == 'Descrição alterada'
    assert subject_alterado.slug == 'slug-alterada'


def test_msg_pag_edicao_subject_concluida(resp_edicao_subject, subject):
    """
    Certifica de que a mensagem de edição concluída com o título do subject
    alterado é exibida para o usuário após a edição com sucesso.
    """
    subject_alterado = Subject.objects.get(id=subject.pk)
    assert_contains(resp_edicao_subject, f'O assunto "<strong>{subject_alterado.title}</strong>" '
                                         f'foi editado com sucesso.')


def test_pag_edicao_subject_concluida(resp_edicao_subject, subject):
    """
    Certifica de que a página que informa a alteração é carregada com sucesso
    após a edição do assunto.
    """
    assert resp_edicao_subject.status_code == 200
    assert resp_edicao_subject.wsgi_request.path == f'/assuntos/adm/edicao/{subject.pk}'
