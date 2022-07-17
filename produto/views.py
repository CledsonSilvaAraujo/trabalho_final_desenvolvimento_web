from curses.ascii import HT
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from categoria.models import Categoria
from produto.context_processors import atualiza_valor_total
from produto.forms import ProdutoForm, QuantidadeForm
from produto.models import Produto




def index(request):
    return render(request, 'produto/index.html')


def lista_produto(request):
    produtos = Produto.objects.all()

    forms = []
    for produto in produtos:
        form = QuantidadeForm(initial={'quantidade': produto.quantidade, 'produto_id': produto.id})
        forms.append(form)

    return render(request, 'produto/lista_produto.html', {'listas':zip(produtos, forms)})



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
            print('produto salvo com sucesso')
            if produto_id:
                messages.add_message(request, messages.INFO, 'Produto alterado com sucesso!')
                del request.session['produto_id']
            else:
                messages.add_message(request, messages.INFO, 'Produto cadastrado com sucesso!')

            print('retornando JSON response')
            return JsonResponse({'produto_id':produto.id,'nome':produto.nome,'preco':produto.preco,'categoria': produto.categoria.nome, 'quantidade': produto.quantidade }, safe=False)
    else:
        try:
            del request.session['produto_id']
        except KeyError:
            pass
        produto_form = ProdutoForm()

    return render(request, 'produto/cadastra_produto.html', {'form': produto_form})


def edita_produto(request):
    if not request.POST:
        return(HttpResponse('Não é POST'))

    form = QuantidadeForm(request.POST)
    if not form.is_valid():
        return(HttpResponse('Formulário inválido'))

    produto_id = form.cleaned_data['produto_id']
    quantidade = form.cleaned_data['quantidade']

    if produto_id:
        produto = get_object_or_404(Produto, pk=produto_id)
        produto.quantidade = quantidade
        produto.save()


       
    return JsonResponse(atualiza_valor_total(request))


def deleta_produto(request):
    if not request.POST:
        return(HttpResponse('Não é POST'))

    form = QuantidadeForm(request.POST)
    if not form.is_valid():
        return(HttpResponse('Formulário inválido'))

    produto_id = form.cleaned_data['produto_id']
    print('produto_id = ' + str(produto_id))
    if produto_id:
        produto = get_object_or_404(Produto, pk=produto_id)
        produto.delete()
        print("produto deletado")

    return JsonResponse(atualiza_valor_total(request))