from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Comodidade(models.Model):
    nome = models.CharField(_("nome da comodidade"), max_length=100, unique=True)
    class Meta:
        verbose_name = _("Comodidade"); verbose_name_plural = _("Comodidades"); ordering = ['nome']
    def __str__(self): return self.nome

class Predio(models.Model):
    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predios', verbose_name=_("proprietário"))
    nome = models.CharField(_("nome do prédio/condomínio"), max_length=255)
    endereco_completo = models.CharField(_("endereço completo"), max_length=255)
    cidade = models.CharField(_("cidade"), max_length=100)
    estado = models.CharField(_("estado (UF)"), max_length=2)
    cep = models.CharField(_("CEP"), max_length=9)
    foto_fachada = models.ImageField(_("foto da fachada"), upload_to='predios/fachadas/%Y/%m/%d/', blank=True, null=True)
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)
    class Meta:
        verbose_name = _("Prédio / Condomínio"); verbose_name_plural = _("Prédios / Condomínios"); ordering = ['nome']
    def __str__(self): return f"{self.nome} - {self.cidade}, {self.estado}"

class Apartamento(models.Model):
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE, related_name='apartamentos', verbose_name=_("prédio / condomínio"))
    proprietario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='meus_apartamentos', verbose_name=_("proprietário"))
    titulo = models.CharField(_("identificador da unidade"), max_length=100)
    descricao = models.TextField(_("descrição da unidade"), blank=True)
    numero_quartos = models.PositiveIntegerField(_("número de quartos"), default=1)
    numero_banheiros = models.PositiveIntegerField(_("número de banheiros"), default=1)
    area_m2 = models.DecimalField(_("área (m²)"), max_digits=7, decimal_places=2)
    preco_diaria = models.DecimalField(_("preço da diária (R$)"), max_digits=10, decimal_places=2)
    foto_principal = models.ImageField(_("foto principal da unidade"), upload_to='apartamentos/fotos_principais/%Y/%m/%d/', blank=True, null=True)
    disponivel = models.BooleanField(_("disponível para aluguel?"), default=True)
    comodidades = models.ManyToManyField(Comodidade, blank=True, verbose_name=_("comodidades da unidade"))
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)
    data_atualizacao = models.DateTimeField(_("data de atualização"), auto_now=True)
    class Meta:
        verbose_name = _("Apartamento / Unidade"); verbose_name_plural = _("Apartamentos / Unidades"); ordering = ['predio', 'titulo']
    def __str__(self): return f"{self.predio.nome} - {self.titulo}"

    def get_foto_principal(self):
        """
        Este metodo encontra a foto principal para o anúncio.
        A ordem de prioridade é:
        1. Uma foto da nova galeria marcada como 'principal'.
        2. Se não houver, a primeira foto da nova galeria.
        3. Se não houver, a foto do campo antigo 'foto_principal'.
        4. Se não houver nenhuma, retorna None.
        """
        foto_marcada_como_principal = self.fotos.filter(principal=True).first()
        if foto_marcada_como_principal:
            return foto_marcada_como_principal.imagem.url

        primeira_foto_da_galeria = self.fotos.first()
        if primeira_foto_da_galeria:
            return primeira_foto_da_galeria.imagem.url

        if self.foto_principal:
            return self.foto_principal.url

        return None  # Retorna None se não houver foto alguma

class Perfil(models.Model):
    class CargoUsuario(models.TextChoices):
        CLIENTE = 'CLIENTE', _('Cliente')
        PROPRIETARIO = 'PROPRIETARIO', _('Proprietário')
        GERENTE = 'GERENTE', _('Gerente')
        FUNCIONARIO = 'FUNCIONARIO', _('Funcionário')
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    cargo = models.CharField(_("cargo"), max_length=20, choices=CargoUsuario.choices, default=CargoUsuario.CLIENTE)
    foto_perfil = models.ImageField(_("foto de perfil"), upload_to='usuarios/fotos_perfil/%Y/%m/%d/', blank=True, null=True)
    telefone = models.CharField(_("telefone"), max_length=20, blank=True)
    bio = models.TextField(_("biografia"), blank=True)
    class Meta:
        verbose_name = _("Perfil de Usuário"); verbose_name_plural = _("Perfis de Usuários")
    def __str__(self): return f"Perfil de {self.usuario.username}"

class Reserva(models.Model):
    class StatusReserva(models.TextChoices):
        PENDENTE = 'PENDENTE', _('Pendente')
        CONFIRMADA = 'CONFIRMADA', _('Confirmada')
        CANCELADA = 'CANCELADA', _('Cancelada')
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, related_name='reservas')
    hospede = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    data_checkin = models.DateField(_("data de check-in"))
    data_checkout = models.DateField(_("data de check-out"))
    status = models.CharField(_("status"), max_length=20, choices=StatusReserva.choices, default=StatusReserva.PENDENTE)
    data_reserva = models.DateTimeField(_("data da reserva"), auto_now_add=True)
    class Meta:
        verbose_name = _("Reserva"); verbose_name_plural = _("Reservas"); ordering = ['-data_reserva']
    def __str__(self): return f"Reserva de {self.apartamento} por {self.hospede.username}"

class Avaliacao(models.Model):
    # A avaliação está ligada a uma única reserva. OneToOneField garante que cada reserva
    # só possa ter uma única avaliação, prevenindo spam.
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name='avaliacao'
    )
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5"
    )
    comentario = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Deixe seu comentário sobre a estadia."
    )
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avaliação de {self.reserva.hospede.username} para {self.reserva.apartamento.titulo}'

class FotoApartamento(models.Model):
    apartamento = models.ForeignKey(
        Apartamento,
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    imagem = models.ImageField(upload_to='apartamentos/fotos/')
    # Este campo nos permite destacar uma foto como a principal do anúncio.
    principal = models.BooleanField(default=False)

    class Meta:
        ordering = ['-principal'] # Garante que a foto principal apareça primeiro

    def __str__(self):
        return f"Foto de {self.apartamento.titulo}"