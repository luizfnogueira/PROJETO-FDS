from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db import models
from .models import Perfil, Hidratacao, IMC, Treino, Exercicio, Sentimento, Atividade, RegistroSaude, Sono, Alimentacao
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
    if request.method == 'POST':
        # Salvar o registro de sono
        horas_dormidas = request.POST.get('hours')
        qualidade_sono = request.POST.get('quality')
        meta_sono = request.POST.get('goal')

        # Cria um novo registro de sono
        novo_registro = Sono(
            user=request.user,  # Associa o registro ao usuário
            horas_dormidas=horas_dormidas,
            qualidade_sono=qualidade_sono,
            meta_sono=meta_sono
        )
        novo_registro.save()

        return redirect('sono')  # Redireciona para a página de registro

    # Obtém os registros de sono do usuário autenticado
    registros = Sono.objects.filter(user=request.user).order_by('-data_registro')
    return render(request, 'html/sono.html', {'registros': registros})


def horassono(request):
    if request.user.is_authenticated:
        registros = Sono.objects.filter(user=request.user).order_by('-data_registro')
    else:
        registros = []

    return render(request, 'html/horassono.html', {'registros': registros})

def alimentacao(request):
    if request.method == "POST":
        preferencias = request.POST.getlist("preferencias")  # Captura múltiplos valores de preferência
        restricoes = request.POST.getlist("restricoes")      # Captura múltiplos valores de restrições
        objetivos = request.POST.get("objetivos", "")

        # Armazenar as informações no banco de dados
        Alimentacao.objects.create(
            preferencias=", ".join(preferencias),  # Salva como string separada por vírgulas
            restricoes=", ".join(restricoes),
            objetivos=objetivos
        )
        
        return redirect('veralimentacao')  # Redireciona para a página de visualização

    return render(request, 'html/alimentacao.html')


def veralimentacao(request):
    ultima_alimentacao = Alimentacao.objects.last()

    # Obter preferências, restrições e objetivos do usuário
    restricoes = ultima_alimentacao.restricoes.split(", ") if ultima_alimentacao else []
    preferencias = ultima_alimentacao.preferencias if ultima_alimentacao else ""
    objetivo = ultima_alimentacao.objetivos if ultima_alimentacao else ""

    # Pratos sugeridos para cada refeição e caso específico
    sugestoes = {
        "cafe_da_manha": {
            "vegano": {
                "hipertrofia": "Pão integral com pasta de amendoim e uma vitamina de frutas com aveia",
                "emagrecimento": "Smoothie de espinafre, banana e aveia com chia",
                "ganho de massa": "Panquecas de aveia e banana com creme de amêndoas",
                "manutencao": "Pão integral com abacate e uma salada de frutas"
            },
            "vegetariano": {
                "hipertrofia": "Omelete de claras com espinafre e queijo cottage",
                "emagrecimento": "Iogurte com frutas vermelhas e uma fatia de pão integral",
                "ganho de massa": "Iogurte grego com granola e frutas",
                "manutencao": "Torrada integral com ovo mexido e queijo branco"
            },
            "carnivoro": {
                "hipertrofia": "Ovos mexidos com peito de peru e uma fatia de pão integral",
                "emagrecimento": "Ovos cozidos com uma fatia de abacate e tomate",
                "ganho de massa": "Omelete de ovos inteiros com peito de frango desfiado",
                "manutencao": "Pão integral com ovos e presunto magro"
            }
        },
        "almoco": {
            "vegano": {
                "hipertrofia": "Quinoa com grão-de-bico, batata doce e vegetais grelhados",
                "emagrecimento": "Salada de folhas verdes, grão-de-bico e vinagrete de limão",
                "ganho de massa": "Arroz integral, feijão preto e tofu grelhado",
                "manutencao": "Arroz integral com legumes cozidos e feijão"
            },
            "vegetariano": {
                "hipertrofia": "Arroz integral, lentilhas e ovos mexidos com espinafre",
                "emagrecimento": "Salada de quinoa com queijo branco e vegetais",
                "ganho de massa": "Risoto de cogumelos e queijo parmesão",
                "manutencao": "Macarrão integral com molho de tomate e queijo cottage"
            },
            "carnivoro": {
                "hipertrofia": "Arroz integral, peito de frango grelhado e brócolis",
                "emagrecimento": "Filé de peixe com salada verde e uma porção pequena de arroz",
                "ganho de massa": "Macarrão integral com almôndegas de carne",
                "manutencao": "Carne bovina magra com batata doce e salada"
            }
        },
        "cafe_da_tarde": {
            "vegano": {
                "hipertrofia": "Shake de proteína vegana com banana e leite de amêndoas",
                "emagrecimento": "Frutas com um punhado de amêndoas",
                "ganho de massa": "Biscoitos de aveia com pasta de amendoim e banana",
                "manutencao": "Hummus com cenoura e pepino fatiados"
            },
            "vegetariano": {
                "hipertrofia": "Iogurte com granola e uma banana",
                "emagrecimento": "Frutas com iogurte desnatado",
                "ganho de massa": "Sanduíche de queijo e tomate",
                "manutencao": "Torrada integral com queijo cottage e frutas"
            },
            "carnivoro": {
                "hipertrofia": "Sanduíche de peito de peru e queijo com pão integral",
                "emagrecimento": "Ovos cozidos e uma maçã",
                "ganho de massa": "Sanduíche de frango desfiado com cenoura ralada",
                "manutencao": "Torrada com requeijão e peito de peru"
            }
        },
        "jantar": {
            "vegano": {
                "hipertrofia": "Batata doce com feijão preto e salada de rúcula",
                "emagrecimento": "Sopa de legumes variados",
                "ganho de massa": "Arroz integral com tofu e brócolis",
                "manutencao": "Salada de grão-de-bico com cenoura e tomate"
            },
            "vegetariano": {
                "hipertrofia": "Omelete de legumes e uma porção de arroz",
                "emagrecimento": "Sopa de abóbora com ervas",
                "ganho de massa": "Lasanha de berinjela com queijo",
                "manutencao": "Risoto de abobrinha e queijo"
            },
            "carnivoro": {
                "hipertrofia": "Peito de frango grelhado com batata doce e espinafre",
                "emagrecimento": "Sopa de frango com legumes",
                "ganho de massa": "Arroz integral, carne moída e brócolis",
                "manutencao": "Frango grelhado com legumes"
            }
        },
        "ceia": {
            "vegano": {
                "hipertrofia": "Shake de proteína vegana com amêndoas",
                "emagrecimento": "Frutas vermelhas e chá de camomila",
                "ganho de massa": "Biscoitos integrais com pasta de amêndoa",
                "manutencao": "Mix de nozes e frutas secas"
            },
            "vegetariano": {
                "hipertrofia": "Iogurte grego com mel",
                "emagrecimento": "Queijo cottage e frutas",
                "ganho de massa": "Iogurte com granola",
                "manutencao": "Torrada integral com requeijão light"
            },
            "carnivoro": {
                "hipertrofia": "Iogurte proteico com mel",
                "emagrecimento": "Frutas frescas e uma porção de amêndoas",
                "ganho de massa": "Queijo cottage com torradas integrais",
                "manutencao": "Leite desnatado com uma torrada integral"
            }
        }
    }

    # Selecionar pratos com base na preferência e objetivo
    sugestao_cafe = sugestoes["cafe_da_manha"].get(preferencias, {}).get(objetivo, "Opção não disponível")
    sugestao_almoco = sugestoes["almoco"].get(preferencias, {}).get(objetivo, "Opção não disponível")
    sugestao_cafe_tarde = sugestoes["cafe_da_tarde"].get(preferencias, {}).get(objetivo, "Opção não disponível")
    sugestao_jantar = sugestoes["jantar"].get(preferencias, {}).get(objetivo, "Opção não disponível")
    sugestao_ceia = sugestoes["ceia"].get(preferencias, {}).get(objetivo, "Opção não disponível")

    contexto = {
        "preferencias": ultima_alimentacao.preferencias if ultima_alimentacao else "",
        "restricoes": ultima_alimentacao.restricoes if ultima_alimentacao else "",
        "objetivos": ultima_alimentacao.objetivos if ultima_alimentacao else "",
        "sugestoes": {
            "cafe_da_manha": sugestao_cafe,
            "almoco": sugestao_almoco,
            "cafe_da_tarde": sugestao_cafe_tarde,
            "jantar": sugestao_jantar,
            "ceia": sugestao_ceia
        }
    }

    return render(request, 'html/veralimentacao.html', contexto)

def suplementacao(request):
    return render(request, 'html/suplementacao.html')

def versuplementacao(request):
    return render(request, 'html/versuplementacao.html')