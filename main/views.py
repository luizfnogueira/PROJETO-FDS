from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db import models
from .models import Perfil, Hidratacao, IMC
from datetime import date


def paginainicial(request):
    return render(request, 'html/PaginaInicial.html')


def login(request):
    return render(request, 'html/login.html')


def home(request):
    return render(request, 'html/home.html')  # Renderiza o template home.html


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        password = request.POST['password']
        cpf = request.POST['cpf']
        data_cadastro = request.POST['data_cadastro']

        # Verifica se o nome de usuário ou CPF já existe
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Nome de usuário já existe!')
            return render(request, 'html/cadastro.html')

        if Perfil.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado!')
            return render(request, 'html/cadastro.html')

        # Criar o usuário no banco de dados
        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()

        # Criar o perfil com CPF e data de cadastro
        perfil = Perfil(user=user, cpf=cpf, data_cadastro=data_cadastro)
        perfil.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')  # Redireciona para a página de login após o cadastro

    return render(request, 'html/cadastro.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar o usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirecionar para a página home após login bem-sucedido
        else:
            return render(request, 'html/login.html', {'error': 'Credenciais inválidas!'})

    return render(request, 'html/login.html')


def logout(request):
    auth_logout(request)  # Faz o logout do usuário
    return redirect('login')  # Redireciona para a página de login após o logout


def hidratacao(request):
    if request.method == 'POST':
        quantidade_agua = int(request.POST['quantidade_agua'])  # Obtém a quantidade de água do formulário
        usuario = request.user  # Obtém o usuário logado
        novo_registro = Hidratacao.objects.create(user=usuario, quantidade_agua=quantidade_agua)
        novo_registro.save()

    # Calcula o total diário de água
    total_diario = Hidratacao.objects.filter(user=request.user, data=date.today()).aggregate(models.Sum('quantidade_agua'))['quantidade_agua__sum'] or 0

    return render(request, 'html/hidratacao.html', {'total_diario': total_diario})


def historico_hidratacao(request):
    # Recupera todos os registros de hidratação do usuário logado
    registros = Hidratacao.objects.filter(user=request.user).order_by('-data')
    return render(request, 'html/historicohidratacao.html', {'registros': registros})


def calculo_imc(request):
    imc = None
    if request.method == 'POST':
        peso = float(request.POST['peso'])
        altura = float(request.POST['altura'])

        # Calcular o IMC
        imc = peso / (altura ** 2)

        # Armazenar o IMC no banco de dados
        novo_imc = IMC.objects.create(user=request.user, peso=peso, altura=altura, imc=imc)
        novo_imc.save()

    return render(request, 'html/meupeso.html', {'imc': imc})