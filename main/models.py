from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)  # CPF com 11 dígitos
    data_cadastro = models.DateField()

    def str(self):
        return self.user.username


class Hidratacao(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o registro ao usuário
    quantidade_agua = models.IntegerField()  # Quantidade de água em ml
    data = models.DateField(auto_now_add=True)  # Data do registro, preenchida automaticamente

    def str(self):
        return f"{self.user.username} - {self.quantidade_agua} ml em {self.data}"
    

class IMC(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona o IMC ao usuário
    peso = models.FloatField()  # Armazena o peso do usuário
    altura = models.FloatField()  # Armazena a altura do usuário
    imc = models.FloatField()  # Armazena o IMC calculado
    data_calculo = models.DateField(auto_now_add=True)  # Data do cálculo, preenchida automaticamente

    def str(self):
        return f"IMC de {self.user.username}: {self.imc}"