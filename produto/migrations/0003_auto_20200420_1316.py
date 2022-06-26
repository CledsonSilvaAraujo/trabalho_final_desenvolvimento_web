# Generated by Django 3.0.2 on 2020-04-20 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_auto_20200319_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='produto',
            name='quantidade',
            field=models.IntegerField(),
        ),
    ]