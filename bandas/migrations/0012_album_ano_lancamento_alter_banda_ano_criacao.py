# Generated by Django 5.1.3 on 2025-04-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bandas", "0011_alter_banda_nacionalidade_alter_musica_duracao"),
    ]

    operations = [
        migrations.AddField(
            model_name="album",
            name="ano_lancamento",
            field=models.IntegerField(
                blank=True, default=2000, null=True, verbose_name="Ano de lançamento"
            ),
        ),
        migrations.AlterField(
            model_name="banda",
            name="ano_criacao",
            field=models.IntegerField(verbose_name="Ano de criação"),
        ),
    ]
