from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from datetime import datetime
from .models import Perfil  # Importa o modelo Perfil


def paginainicial(request):
    return render(request, 'html/PaginaInicial.html')


def login(request):
    return render(request, 'html/login.html')


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
        # Obter o nome de usuário e a senha do formulário
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar o usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Se a autenticação for bem-sucedida, fazer login
            auth_login(request, user)
            return redirect('inicio')  # Redirecionar para a página inicial ou dashboard
        else:
            # Se a autenticação falhar, exibir mensagem de erro
            return render(request, 'html/login.html', {'error': 'Credenciais inválidas!'})

    return render(request, 'html/login.html')