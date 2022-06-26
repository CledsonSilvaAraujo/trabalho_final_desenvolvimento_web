from django.contrib import admin
from .models import Produto

class ProdutoAdmin(admin.ModelAdmin):
    fields = ('categoria', 'nome', 'slug', 'quantidade', 'preco')
    list_display = ['nome', 'slug', 'categoria', 'quantidade', 'preco']
    search_fields = ['nome']
    list_filter = ['categoria']
    list_editable = ['categoria', 'quantidade', 'preco']
    prepopulated_fields = {'slug': ('nome',)}

admin.site.register(Produto, ProdutoAdmin)
