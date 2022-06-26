from django.db import models
from django.urls import reverse

from categoria.models import Categoria

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='produtos', on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField(max_length=100)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table='produto'

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('carrinho:exibe_produto', args=[self.id, self.slug])






