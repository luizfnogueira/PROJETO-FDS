from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.db import models
from .models import Perfil, Hidratacao, IMC, Treino, Exercicio, Sentimento, Atividade, RegistroSaude, Sono, Alimentacao, Suplementacao, TreinoPersonalizado
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
    preferencias = ultima_alimentacao.preferencias.split(", ") if ultima_alimentacao else []
    objetivo = ultima_alimentacao.objetivos if ultima_alimentacao else "manutencao"  # padrão caso nenhum objetivo seja fornecido

    # Dicionário de sugestões para cada refeição e objetivo
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
            "geral": {
                "hipertrofia": "Ovos mexidos com abacate e pão integral",
                "emagrecimento": "Iogurte natural com frutas e aveia",
                "ganho de massa": "Panqueca de banana com aveia e pasta de amendoim",
                "manutencao": "Pão integral com queijo branco e uma vitamina de frutas"
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
            "geral": {
                "hipertrofia": "Frango grelhado com batata doce e salada de folhas",
                "emagrecimento": "Peito de frango com brócolis e legumes ao vapor",
                "ganho de massa": "Arroz integral, feijão e carne moída",
                "manutencao": "Arroz, feijão, carne grelhada e salada"
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
            "geral": {
                "hipertrofia": "Iogurte grego com aveia e frutas",
                "emagrecimento": "Frutas com um punhado de nozes",
                "ganho de massa": "Sanduíche de peito de peru com queijo",
                "manutencao": "Torrada com requeijão e uma fruta"
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
            "geral": {
                "hipertrofia": "Frango grelhado com arroz integral e vegetais",
                "emagrecimento": "Sopa de legumes e uma fatia de pão integral",
                "ganho de massa": "Arroz, feijão e carne moída com vegetais",
                "manutencao": "Sopa de legumes com carne e torradas"
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
            "geral": {
                "hipertrofia": "Iogurte grego com frutas e aveia",
                "emagrecimento": "Chá de camomila com mix de frutas vermelhas",
                "ganho de massa": "Mix de castanhas e frutas secas",
                "manutencao": "Mix de nozes e uma fruta"
            }
        }
    }

    # Gerar sugestões de pratos com base nas preferências e objetivos
    pratos_sugeridos = {}
    if "naotenho" in preferencias and "nao" in restricoes:
        # Retorna sugestões gerais para cada refeição com base no objetivo
        for refeicao, opcoes in sugestoes.items():
            pratos_sugeridos[refeicao] = opcoes["geral"].get(objetivo, "Sugestão não disponível")
    else:
        # Gera sugestões baseadas nas preferências e objetivos
        for refeicao, opcoes in sugestoes.items():
            prato = None
            for preferencia in preferencias:
                if preferencia in opcoes:
                    prato = opcoes[preferencia].get(objetivo, opcoes[preferencia].get('manutencao'))
                    if prato:
                        break
            pratos_sugeridos[refeicao] = prato or opcoes["geral"].get(objetivo, "Nenhuma sugestão disponível")

    # Adicionar variáveis ao contexto
    return render(request, 'html/veralimentacao.html', {
        'pratos_sugeridos': pratos_sugeridos,
        'preferencias': ", ".join(preferencias),
        'restricoes': ", ".join(restricoes),
        'objetivo': objetivo
    })

def suplementacao_view(request):
    suplementos = Suplementacao.objects.filter(usuario=request.user)
    return render(request, 'html/versuplementacao.html', {'suplementos': suplementos})

def adicionar_suplementacao(request):
    if request.method == "POST":
        nome = request.POST.get("nome")
        quantidade = request.POST.get("quantidade")
        horario = request.POST.get("horario")

        Suplementacao.objects.create(
            usuario=request.user,
            nome=nome,
            quantidade=quantidade,
            horario=horario
        )
        return redirect('versuplementacao')

    return render(request, 'html/versuplementacao.html')

def criartreino(request):
    # Lógica para a view criartreino
    return render(request, 'html/criartreino.html')

def gerar_treino(objetivo):
    if objetivo == 'hipertrofia':
        return """
            1. Supino com barra - 4x8-10 repetições
            2. Agachamento livre - 4x10 repetições
            3. Remada curvada - 4x10 repetições
            4. Desenvolvimento com halteres - 4x10 repetições
            5. Leg press - 4x10 repetições
            6. Rosca direta com barra - 3x12 repetições
            7. Tríceps pulley - 3x12 repetições
            8. Elevação lateral - 3x15 repetições
            9. Panturrilha no leg press - 4x15 repetições
            10. Abdominais (crunch) - 3x20 repetições
            Descanso: 60-90 segundos entre séries.
        """
    elif objetivo == 'emagrecimento':
        return """
            1. Corrida na esteira - 5 minutos de aquecimento
            2. Circuito de burpees - 3x15 repetições
            3. Polichinelos - 3x20 repetições
            4. Agachamento com salto - 4x15 repetições
            5. Flexões de braço - 3x12 repetições
            6. Mountain climbers - 3x30 segundos
            7. Jumping lunges - 4x12 repetições
            8. Abdominais bicicleta - 3x20 repetições
            9. Prancha - 3x1 minuto
            10. Corda de pular - 5 minutos para finalização
            Descanso: 30 segundos entre os exercícios.
        """
    elif objetivo == 'ganho de massa':
        return """
            1. Supino inclinado com halteres - 4x8-10 repetições
            2. Levantamento terra - 4x8-10 repetições
            3. Agachamento sumô - 4x10 repetições
            4. Desenvolvimento militar - 4x8 repetições
            5. Remada alta com barra - 3x10 repetições
            6. Extensão de pernas na máquina - 4x12 repetições
            7. Flexão de pernas - 4x12 repetições
            8. Rosca alternada com halteres - 3x10 repetições
            9. Tríceps francês - 3x10 repetições
            10. Panturrilha sentado - 4x15 repetições
            Descanso: 60-90 segundos entre séries.
        """
    elif objetivo == 'manutencao':
        return """
            1. Supino reto com halteres - 3x12 repetições
            2. Agachamento com halteres - 3x15 repetições
            3. Remada unilateral com halteres - 3x12 repetições
            4. Desenvolvimento lateral - 3x15 repetições
            5. Rosca scott - 3x12 repetições
            6. Tríceps testa com halteres - 3x12 repetições
            7. Elevação pélvica - 3x15 repetições
            8. Abdominais - 3x20 repetições
            9. Cadeira extensora - 3x15 repetições
            10. Panturrilha em pé - 4x20 repetições
            Descanso: 60 segundos entre séries.
        """
    elif objetivo == 'resistencia':
        return """
            1. Burpees - 3x20 repetições
            2. Agachamento com salto - 3x15 repetições
            3. Flexão de braço - 3x15 repetições
            4. Mountain climbers - 3x1 minuto
            5. Corrida ou caminhada em alta inclinação - 5 minutos
            6. Prancha lateral - 3x30 segundos de cada lado
            7. Elevação de pernas - 3x20 repetições
            8. Remada com elástico - 3x20 repetições
            9. Salto em caixa - 3x15 repetições
            10. Prancha alta - 3x1 minuto
            Descanso: 30 segundos entre séries.
        """
    return "Treino não encontrado."

def criartreino(request):
    if request.method == "POST":
        objetivo = request.POST.get("objetivos")
        
        # Gera o treino com base no objetivo
        treino_sugerido = gerar_treino(objetivo)

        # Salva a preferência e o treino sugerido no banco de dados
        TreinoPersonalizado.objects.create(user=request.user, objetivo=objetivo, treino_sugerido=treino_sugerido)
        
        # Redireciona para a página de treino personalizado
        return redirect('treinopersonalizado')

    return render(request, 'html/criartreino.html')

def treinopersonalizado(request):
    # Recupera o último treino personalizado do usuário
    treino = TreinoPersonalizado.objects.filter(user=request.user).last()
    
    return render(request, 'html/treinopersonalizado.html', {'treino': treino})