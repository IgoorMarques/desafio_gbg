from django.db import models
from django.contrib.auth.models import AbstractUser


# Modelo de Usuário
class Usuario(AbstractUser):
    class FuncaoChoices(models.TextChoices):
        TECNICO = 'Tecnico', 'Técnico'
        ENFERMAGEM = 'Enfermagem', 'Enfermagem'
        ADMINISTRATIVO = 'Administrativo', 'Administrativo'

    funcao = models.CharField(
        max_length=20,
        choices=FuncaoChoices.choices,
        default=FuncaoChoices.TECNICO
    )

    def __str__(self):
        return f"{self.username} ({self.funcao})"


# Modelo de Material
class Material(models.Model):
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)
    data_validade = models.DateField()
    serial = models.CharField(max_length=100, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.serial:
            self.serial = f"{self.nome[:3].upper()}-{self.id or 'NEW'}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.serial


# Modelo de Processo
class Processo(models.Model):
    class EtapaChoices(models.TextChoices):
        RECEBIMENTO = 'Recebimento', 'Recebimento'
        LAVAGEM = 'Lavagem', 'Lavagem'
        ESTERILIZACAO = 'Esterilização', 'Esterilização'
        DISTRIBUICAO = 'Distribuição', 'Distribuição'

    class StatusChoices(models.TextChoices):
        PENDENTE = 'Pendente', 'Pendente'
        FINALIZADO = 'Finalizado', 'Finalizado'
        FALHA = 'Falha', 'Falha'

    etapa = models.CharField(
        max_length=20,
        choices=EtapaChoices.choices
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE
    )
    data_hora = models.DateTimeField(auto_now_add=True)
    serial_material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name='processos'
    )
    usuario_responsavel = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name='processos'
    )

    def __str__(self):
        return f"{self.serial_material.serial} - {self.etapa} ({self.status})"
