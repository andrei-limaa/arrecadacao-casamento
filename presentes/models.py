from django.db import models

class Contribuicao(models.Model):

    STATUS_CHOICES = (
        ('Pendente', 'Pendente'),
        ('Pago', 'Pago'),
        ('Cancelado', 'Cancelado'),
    )

    nome = models.CharField(max_length=100)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pendente'
    )

    pagamento_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )

    pix_code = models.TextField(
        blank=True,
        null=True
    )

    qr_code = models.TextField(
        blank=True,
        null=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.nome} - R$ {self.valor} - {self.status}"