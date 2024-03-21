from sendgrid import SendGridAPIClient
from mcfields import settings
from mcfields.newsletter.models import Newsletter


def listar_newsletters_ordenadas():
    """
    Busca as newsletters no banco de dados e as retorna de maneira ordenada pela data de publicação (reversamente).
    """
    ordered_newsletters = Newsletter.objects.order_by('-pub_date').all()
    return list(ordered_newsletters)


def criar_rascunho(key, titulo, list_id, design_id):
    """
    Cria um rascunho de email no SendGrid relacionado com a newsletter editada ou postada.
    :param key: SENDGRID_API_KEY;
    :param titulo: Título da newsletter editada ou postada;
    :param list_id: ID da lista de contatos que receberão o email (SENDGRID_LIST_ID);
    :param design_id: ID do modelo de email criado para newsletters (SENDGRID_NEWSLETTER_DESIGN_ID);
    :return: Requisição no site do SendGrid criando o rascunho.
    """
    sg = SendGridAPIClient(key)
    data = {
        'name': f'Nova newsletter: {titulo}',
        'send_to': {'list_ids': [list_id]},
        'email_config': {'design_id': design_id,
                         'suppression_group_id': settings.SUPPRESSION_GROUP_ID,
                         'sender_id': settings.SENDER_ID}
    }
    return sg.client.marketing.singlesends.post(request_body=data)
