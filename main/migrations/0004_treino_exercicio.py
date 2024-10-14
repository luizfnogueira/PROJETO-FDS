# Generated by Django 5.1.1 on 2024-10-14 14:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_imc'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Treino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_da_semana', models.CharField(choices=[('segunda', 'Segunda-feira'), ('terca', 'Terça-feira'), ('quarta', 'Quarta-feira'), ('quinta', 'Quinta-feira'), ('sexta', 'Sexta-feira'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('series', models.PositiveIntegerField()),
                ('repeticoes', models.PositiveIntegerField()),
                ('treino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercicios', to='main.treino')),
            ],
        ),
    ]
