from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True) 
    data_cadastro = models.DateField()

    def str(self):
        return self.user.username


class Hidratacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o registro ao usuário
    quantidade_agua = models.IntegerField()  # 
    data = models.DateField(auto_now_add=True) 

    def str(self):
        return f"{self.user.username} - {self.quantidade_agua} ml em {self.data}"
    

class IMC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o IMC ao usuário
    peso = models.FloatField()  
    altura = models.FloatField() 
    imc = models.FloatField() 
    data_calculo = models.DateField(auto_now_add=True) 

    def str(self):
        return f"IMC de {self.user.username}: {self.imc}"
    

class Treino(models.Model):
    DIAS_DA_SEMANA = [
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o treino ao usuário
    dia_da_semana = models.CharField(max_length=10, choices=DIAS_DA_SEMANA)  # Escolhe o dia da semana

    def str(self):
        return f"{self.user.username} - Treino de {self.get_dia_da_semana_display()}"

class Exercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE, related_name="exercicios")  # Relaciona ao treino
    nome = models.CharField(max_length=100) 
    series = models.PositiveIntegerField() 
    repeticoes = models.PositiveIntegerField()

    def str(self):
        return f"{self.nome} - {self.series} séries de {self.repeticoes} repetições"

class Atividade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class Sentimento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    sentimento = models.CharField(max_length=100)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.atividade} - {self.sentimento}"

class RegistroSaude(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o registro ao usuário
    sintoma = models.CharField(max_length=255, blank=True, null=True)
    intensidade = models.CharField(max_length=50)
    area = models.CharField(max_length=255, blank=True, null=True)
    medicamento = models.CharField(max_length=255, blank=True, null=True)
    medico = models.CharField(max_length=255, blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sintoma} - {self.intensidade} por {self.user.username}"
    
class Sono(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)  # Adicione null=True temporariamente
    horas_dormidas = models.IntegerField()
    qualidade_sono = models.IntegerField()
    meta_sono = models.TextField()
    data_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sono: {self.horas_dormidas} horas, Qualidade: {self.qualidade_sono}"
    
class Alimentacao(models.Model):
    preferencias = models.TextField()
    restricoes = models.TextField()
    objetivos = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Objetivo: {self.objetivos}"
    
class Suplementacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    quantidade = models.CharField(max_length=50)
    horario = models.TimeField()

    def __str__(self):
        return f"{self.nome} - {self.quantidade} ({self.horario})"

class TreinoPersonalizado(models.Model):
    OBJETIVOS = [
        ('hipertrofia', 'Hipertrofia'),
        ('emagrecimento', 'Emagrecimento'),
        ('ganho de massa', 'Ganho de Massa Muscular'),
        ('manutencao', 'Manutenção de Peso'),
        ('resistencia', 'Melhorar Resistência'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objetivo = models.CharField(max_length=20, choices=OBJETIVOS)
    treino_sugerido = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.objetivo}'