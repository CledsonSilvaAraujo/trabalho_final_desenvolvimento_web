from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, request, JsonResponse
from django.middleware import locale
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify

from carrinho.carrinho import Carrinho
from carrinho.forms import QuantidadeForm
from carrinho.views import signer
from categoria.models import Categoria
from produto.forms import PesquisaProdutoForm, ProdutoForm
from produto.models import Produto


def atualiza_carrinho(request):
    form = QuantidadeForm(request.POST)
    if form.is_valid():
        produto_id = signer.unsign(form.cleaned_data['produto_id'])
        quantidade = form.cleaned_data['quantidade']

        carrinho = Carrinho(request)
        if (quantidade == 0):
            carrinho.remover(produto_id)
            preco_total = 0.0
        else:
            carrinho.atualiza(produto_id, quantidade)
            preco_total = carrinho.get_preco_total(produto_id)

        qtd = carrinho.get_quantidade_carrinho()
        preco_carrinho = carrinho.get_preco_carrinho()

        print('***** id do produto = ' + produto_id +
              '  quantidade = ' + str(quantidade) +
              '  preço total do produto = ' + str(preco_total))
        print('***** qtd no carrinho = ' + str(qtd) +
              '  valor do carrinho = ' + str(preco_carrinho))

        locale.setlocale(locale.LC_ALL, 'pt_BR')
        preco_carrinho = locale.currency(preco_carrinho, grouping=True)
        preco_total = Decimal(preco_total)
        preco_total = locale.currency(preco_total, grouping=True)

        return JsonResponse({'quantidade': qtd,
                             'preco_carrinho': preco_carrinho,
                             'preco_total': preco_total})
    else:
        raise ValueError('Ocorreu um erro inesperado ao adicionar um produto ao carrinho.')


def lista_produto(request, slug_da_categoria=None):
    categoria = None
    categorias = Categoria.objects.all().order_by('nome')
    lista_de_produtos = Produto.objects.order_by('nome')
    if slug_da_categoria:
        categoria = get_object_or_404(Categoria, slug=slug_da_categoria)
        lista_de_produtos = lista_de_produtos.filter(categoria=categoria).order_by('nome')
        print(lista_de_produtos)

    paginator = Paginator(lista_de_produtos, 12)
    pagina = request.GET.get('pagina')
    try:
        produtos = paginator.page(pagina)
    except PageNotAnInteger:
        produtos = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        produtos = paginator.page(paginator.num_pages)

    carrinho = Carrinho(request)
    lista_de_forms = []
    for produto in produtos:
        qtd = carrinho.get_quantidade_total(produto.id)
        lista_de_forms.append(QuantidadeForm(initial={'quantidade': qtd, 'produto_id': signer.sign(produto.id)}))

    if request.is_ajax():
        return render(request, 'produto/index.html', {'listas': zip(produtos, lista_de_forms)})

    return render(request, 'produto/index.html', {'categorias': categorias,
                                                            'listas': zip(produtos, lista_de_forms),
                                                            'categoria': categoria})


def cadastra_produto(request):
    if request.POST:
        produto_id = request.session.get('produto_id')
        print('produto_id na sessão = ' + str(produto_id))
        if produto_id:
            produto = get_object_or_404(Produto, pk=produto_id)
            produto_form = ProdutoForm(request.POST, request.FILES, instance=produto)
        else:
            produto_form = ProdutoForm(request.POST, request.FILES)

        if produto_form.is_valid():
            produto = produto_form.save(commit=False)
            produto.slug = slugify(produto.nome)
            produto.save()
            if produto_id:
                messages.add_message(request, messages.INFO, 'Produto alterado com sucesso!')
                del request.session['produto_id']
            else:
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso!')
            lista_produto(request)
            return render(request, 'produto/index.html', {'form': produto_form})
    else:
        try:
            del request.session['produto_id']
        except KeyError:
            pass
        produto_form = ProdutoForm()
    lista_produto(request)
    return render(request, 'produto/index.html', {'form': produto_form})


def exibe_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    request.session['produto_id_del'] = id
    return render(request, 'produto/index.html', {'produto': produto})


def edita_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto_form = ProdutoForm(instance=produto)
    request.session['produto_id'] = id
    return render(request, 'produto/index.html', {'form': produto_form})


def remove_produto(request):
    produto_id = request.session.get('produto_id_del')
    produto = get_object_or_404(Produto, id=produto_id)
    produto.delete()
    del request.session['produto_id_del']
    messages.add_message(request, messages.INFO, 'Produto removido com sucesso.')
    return render(request, 'produto/exibe_produto.html', {'produto': produto})




def index(request):
    try:
        del request.session['produto_id']
    except KeyError:
        pass
    produto_form = ProdutoForm()

    return render(request, 'produto/index.html', {'form': produto_form})

def exibe_carrinho(request):
    carrinho = Carrinho(request)
    produtos_no_carrinho = carrinho.get_produtos()

    lista_de_forms = []
    for produto in produtos_no_carrinho:
        lista_de_forms.append(QuantidadeForm(
            initial = {'quantidade': produto['quantidade'],
                       'produto_id': signer.sign(produto['id'])}
        ))
    valor_do_carrinho = carrinho.get_preco_carrinho()

    return render (request, 'carrinho/produtos_no_carrinho.html', {
        'listas': zip(produtos_no_carrinho, lista_de_forms),
        'valor_do_carrinho': valor_do_carrinho
    })



