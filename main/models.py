from django.db import models
from django.contrib.auth.models import User

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