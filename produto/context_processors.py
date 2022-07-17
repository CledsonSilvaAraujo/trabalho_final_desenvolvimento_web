

from produto.models import Produto


def atualiza_valor_total(request):
    
    produtos = Produto.objects.all()

    valor_total = sum([produto.preco * produto.quantidade for produto in produtos])

    return {
        'valor_total': valor_total
    }