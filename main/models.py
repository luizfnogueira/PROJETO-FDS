from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)  # CPF com 11 dígitos
    data_cadastro = models.DateField()

    def str(self):
        return self.user.username