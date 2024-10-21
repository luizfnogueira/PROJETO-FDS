from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db import models
from .models import Perfil, Hidratacao, IMC, Treino, Exercicio, Sentimento, Atividade, RegistroSaude, Sono
from datetime import date



def paginainicial(request):
    return render(request, 'html/PaginaInicial.html')


def login(request):
    return render(request, 'html/login.html')


def home(request):
    return render(request, 'html/home.html') 


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

        user = User.objects.create_user(username=nome, email=email, password=password)
        user.save()

        perfil = Perfil(user=user, cpf=cpf, data_cadastro=data_cadastro)
        perfil.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login') 

    return render(request, 'html/cadastro.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar o usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home') 
        else:
            return render(request, 'html/login.html', {'error': 'Credenciais inválidas!'})

    return render(request, 'html/login.html')


def logout(request):
    auth_logout(request) 
    return redirect('login')

def hidratacao(request):
    if request.method == 'POST':
        quantidade_agua = int(request.POST['quantidade_agua'])  
        usuario = request.user 
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

        imc = peso / (altura ** 2)

        # Armazenar o IMC no banco de dados
        novo_imc = IMC.objects.create(user=request.user, peso=peso, altura=altura, imc=imc)
        novo_imc.save()

    return render(request, 'html/meupeso.html', {'imc': imc})


def adicionar_treino(request):
    if request.method == 'POST':
        dia_da_semana = request.POST['dia_da_semana']

        # Cria o treino para o dia especificado
        novo_treino = Treino.objects.create(user=request.user, dia_da_semana=dia_da_semana)

        # Adiciona os exercícios ao treino
        for i in range(len(request.POST.getlist('nome_exercicio'))):
            nome = request.POST.getlist('nome_exercicio')[i]
            series = int(request.POST.getlist('series')[i])
            repeticoes = int(request.POST.getlist('repeticoes')[i])
            Exercicio.objects.create(treino=novo_treino, nome=nome, series=series, repeticoes=repeticoes)

        return redirect('meustreinos')  # Redireciona para a página de treinos

    return render(request, 'html/adicionartreino.html')


def ver_treinos(request):
    # Busca os treinos do usuário logado
    treinos = Treino.objects.filter(user=request.user).order_by('dia_da_semana')
    return render(request, 'html/meustreinos.html', {'treinos': treinos})


def remover_treino(request, treino_id):
    # Obtém o treino pelo ID e garante que o usuário logado seja o proprietário
    treino = get_object_or_404(Treino, id=treino_id, user=request.user)

    treino.delete()

    return redirect('meustreinos')

def sentimento(request):
    if request.method == 'POST':
        atividade_texto = request.POST['atividade']
        sentimento_texto = request.POST['sentimento']
        usuario = request.user

        # Verifica se a atividade já existe, senão cria uma nova
        atividade, created = Atividade.objects.get_or_create(nome=atividade_texto)

        # Criar um novo registro de sentimento
        sentimento = Sentimento.objects.create(usuario=usuario, atividade=atividade, sentimento=sentimento_texto)
        sentimento.save()

        # Mensagem de sucesso
        messages.success(request, 'Seu sentimento foi registrado com sucesso!')

        return redirect('sentimento')  # Redirecionar para a mesma página

    return render(request, 'html/sentimento.html')

def historico_humor(request):
    # Busca todos os registros de sentimento do usuário
    registros = Sentimento.objects.filter(usuario=request.user).select_related('atividade').order_by('-data')
    return render(request, 'html/historicohumor.html', {'registros': registros})

def alongamento(request):
    return render(request, 'html/alongamento.html')

def relaxamentomuscular(request):
    return render(request, 'html/relaxamentomuscular.html')

def respiracaoguiada(request):
    return render(request, 'html/respiracaoguiada.html')

def tecnicaspbemestar(request):
    return render(request, 'html/tecnicaspbemestar.html')

def saude(request):
    if request.method == "POST":
        sintoma = request.POST.get("sintoma")
        intensidade = request.POST.get("intensidade")
        area = request.POST.get("area")
        medicamento = request.POST.get("medicamento")
        medico = request.POST.get("medico")

        if request.user.is_authenticated:
            # Cria um novo registro de saúde se o usuário estiver autenticado
            RegistroSaude.objects.create(
                user=request.user,
                sintoma=sintoma,
                intensidade=intensidade,
                area=area,
                medicamento=medicamento,
                medico=medico
            )
            return redirect('saude')  # Redireciona para a página de saúde após o registro
        else:
            return redirect('login')  # Redireciona para a página de login se não autenticado

    return render(request, 'html/saude.html')  # Retorna o formulário se não for um POST

def registrosaude(request):
    if request.user.is_authenticated:
        # Filtra os registros pelo usuário autenticado
        registros = RegistroSaude.objects.filter(user=request.user).order_by('-data')
    else:
        registros = []  # Se o usuário não estiver autenticado, retorna uma lista vazia

    return render(request, 'html/registrosaude.html', {'registros': registros})

def sono(request):
    return render(request, 'html/sono.html')

def horassono(request):
    return render(request, 'html/horassono.html')

def sono(request):
    if request.method == "POST":
        horas_dormidas = int(request.POST.get('hours'))
        qualidade_sono = int(request.POST.get('quality'))
        meta_sono = request.POST.get('goal')

        # Salvar no banco de dados
        novo_registro = Sono(horas_dormidas=horas_dormidas, qualidade_sono=qualidade_sono, meta_sono=meta_sono)
        novo_registro.save()

        return redirect('horassono')  # Redireciona para a página de visualização

    return render(request, 'html/sono.html')

def horassono(request):
    registros = Sono.objects.all().order_by('-data_registro')  # Exibe os registros mais recentes primeiro
    return render(request, 'html/horassono.html', {'registros': registros})

