# Generated by Django 4.0.5 on 2022-06-24 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_cliente_sobrenome_alter_cliente_bairro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(default='', max_length=11),
        ),
    ]