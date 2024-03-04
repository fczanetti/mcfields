from mcfields.newsletter.models import Newsletter


def listar_newsletters_ordenadas():
    """
    Busca as newsletters no banco de dados e as retorna de maneira ordenada pela data de publicação (reversamente).
    """
    ordered_newsletters = Newsletter.objects.order_by('-pub_date').all()
    return list(ordered_newsletters)
