from django.db.models import Prefetch
from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from mcfields.base.models import Subject, Contact
from mcfields.newsletter.models import Newsletter
from mcfields.videos.models import Video


def buscar_subjects_com_conteudos():
    """
    Busca os subjects (assuntos) com os vídeos relacionados. Os vídeos
    são retornados reversamente ordenados pela data de publicação/postagem.
    """
    videos = Video.objects.order_by('-post_date')
    newsletters = Newsletter.objects.order_by('-pub_date')
    subs = Subject.objects.order_by('order').prefetch_related(
        Prefetch('video_set', queryset=videos, to_attr='videos'),
        Prefetch('newsletter_set', queryset=newsletters, to_attr='newsletters')).all()
    return subs


def cadastrar_email(key, user_email, list_id):
    """
    Cadastra um email na plataforma SendGrid para receber novos conteúdos publicados.
    :param key: SENDGRID_API_KEY
    :param user_email: Email a ser cadastrado.
    :param list_id: Lista onde o email será cadastrado (SENDGRID_LIST_ID).
    :return: Requisição de cadastro de email.
    """
    sg = SendGridAPIClient(key)
    data = {"contacts": [{"email": user_email}], 'list_ids': [list_id]}
    return sg.client.marketing.contacts.put(request_body=data)


def checar_email_descadastrado(key, email, suppr_group_id):
    """
    Verifica se o email foi descadastrado anteriormente. Caso tenha sido, este email retornará
    no corpo (body) da resposta da requisição.
    :param key: SENDGRID_API_KEY
    :param email: Email a ser verificado.
    :param suppr_group_id: ID do grupo onde usuários que se descadastraram são inseridos (SUPPRESSION_GROUP_ID).
    :return: Resposta da requisição feita na plataforma SendGrid.
    """
    sg = SendGridAPIClient(key)
    data = {"recipient_emails": [email]}
    response = sg.client.asm.groups._(suppr_group_id).suppressions.search.post(request_body=data)
    return response


def remover_da_lista_desc(key, email, supp_group_id):
    """
    Remove o email da lista de emails descadastrados, possibilitando que este
    receba notificações novamente.
    :param key: SENDGRID_API_KEY.
    :param email: Email a ser removido da lista de emails descadastrados.
    :param supp_group_id: ID do grupo onde usuários que se descadastraram são inseridos (SUPPRESSION_GROUP_ID)..
    """
    sg = SendGridAPIClient(key)
    return sg.client.asm.groups._(supp_group_id).suppressions._(email).delete()


def enviar_mensagem(key, name, email, subject, message, from_email, to_email):
    """
    Envia um email através da API do SendGrid com as informações preenchidas no formulário de contato.
    :param from_email: FROM_EMAIL;
    :param to_email: TO_EMAIL;
    :param key: SENDGRID_API_KEY;
    :param name: Nome do usuário que preencheu o formulário;
    :param email: Email que será usado para retornar a mensagem enviada;
    :param subject: Assunto mencionado no formulário de contato, e também o assunto do email;
    :param message: Mensagem inserida no formulário de contato;
    :return: Envio do email.
    """
    sg = SendGridAPIClient(key)
    context = {'name': name, 'email': email, 'message': message}
    msg = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=render_to_string('base/msg_form_contato.html', context=context)
    )
    return sg.send(msg)


def listar_mensagens_recebidas():
    """
    Retorna todas as mensagens recebidas através do formulário de contato. As mensagens devem vir ordenadas
    inversamente pela data de envio.
    :return:
    """
    return Contact.objects.order_by('-send_date').all()
