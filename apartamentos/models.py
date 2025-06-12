# apartamentos/models.py
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Comodidade(models.Model):
    # O modelo Comodidade permanece o mesmo.
    nome = models.CharField(
        _("nome da comodidade"),
        max_length=100,
        unique=True,
        help_text=_("Ex: Wi-Fi, Ar Condicionado, Piscina, Garagem")
    )

    class Meta:
        verbose_name = _("Comodidade")
        verbose_name_plural = _("Comodidades")
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Predio(models.Model):
    nome = models.CharField(_("nome do prédio/condomínio"), max_length=255, unique=True)
    endereco_completo = models.CharField(_("endereço completo"), max_length=255)
    cidade = models.CharField(_("cidade"), max_length=100)
    estado = models.CharField(_("estado (UF)"), max_length=2, help_text=_("Ex: BA, SP, RJ"))
    cep = models.CharField(_("CEP"), max_length=9, help_text=_("Formato: 12345-678"))
    foto_fachada = models.ImageField(
        _("foto da fachada"),
        upload_to='predios/fachadas/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text=_("Foto da fachada do prédio ou condomínio.")
    )
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)

    class Meta:
        verbose_name = _("Prédio / Condomínio")
        verbose_name_plural = _("Prédios / Condomínios")
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cidade}, {self.estado}"

class Apartamento(models.Model):
    predio = models.ForeignKey(
        Predio,
        on_delete=models.CASCADE, # Se o prédio for deletado, os apartamentos também são.
        related_name='apartamentos',
        verbose_name=_("prédio / condomínio")
    )
    # Título agora pode ser o número/identificador da unidade
    titulo = models.CharField(
        _("identificador da unidade"),
        max_length=100,
        help_text=_("Ex: Apto 101, Bloco A - Apto 204, Casa 3B")
    )
    # Os campos de endereço foram MOVIDOS para o modelo Predio
    # endereco_completo, cidade, estado, cep -> REMOVIDOS
    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='meus_apartamentos', # Renomeado para evitar conflito
        verbose_name=_("proprietário")
    )
    descricao = models.TextField(
        _("descrição da unidade"),
        blank=True,
        help_text=_("Descreva detalhes específicos desta unidade, se houver.")
    )
    numero_quartos = models.PositiveIntegerField(_("número de quartos"), default=1)
    numero_banheiros = models.PositiveIntegerField(_("número de banheiros"), default=1)
    area_m2 = models.DecimalField(_("área (m²)"), max_digits=7, decimal_places=2)
    preco_diaria = models.DecimalField(_("preço da diária (R$)"), max_digits=10, decimal_places=2)
    foto_principal = models.ImageField(
        _("foto principal da unidade"),
        upload_to='apartamentos/fotos_principais/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text=_("A foto de capa do anúncio desta unidade.")
    )
    disponivel = models.BooleanField(_("disponível para aluguel?"), default=True)
    comodidades = models.ManyToManyField(Comodidade, blank=True, verbose_name=_("comodidades da unidade"))
    data_cadastro = models.DateTimeField(_("data de cadastro"), auto_now_add=True)
    data_atualizacao = models.DateTimeField(_("data de atualização"), auto_now=True)

    class Meta:
        verbose_name = _("Apartamento / Unidade")
        verbose_name_plural = _("Apartamentos / Unidades")
        # Garante que um apartamento seja único dentro de um prédio
        unique_together = ('predio', 'titulo')
        ordering = ['predio', 'titulo']

    def __str__(self):
        return f"{self.predio.nome} - {self.titulo}"

class FotoApartamento(models.Model):
    apartamento = models.ForeignKey(
        Apartamento,
        on_delete=models.CASCADE,
        related_name='fotos',
        verbose_name=_("apartamento")
    )
    imagem = models.ImageField(
        _("imagem"),
        upload_to='apartamentos/galeria/%Y/%m/%d/',
        help_text=_("Envie uma imagem da galeria do apartamento.")
    )
    legenda = models.CharField(_("legenda da foto"), max_length=150, blank=True, null=True)
    data_upload = models.DateTimeField(_("data do upload"), auto_now_add=True)

    class Meta:
        verbose_name = _("Foto do Apartamento")
        verbose_name_plural = _("Fotos dos Apartamentos")
        ordering = ['data_upload']

    def __str__(self):
        return f"Foto de {self.apartamento}"

class Perfil(models.Model):
    # O link OneToOne garante que cada usuário tenha apenas um perfil, e vice-versa.
    # CASCADE significa que se o usuário for deletado, seu perfil também será.
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil', # Como acessar o perfil a partir de um usuário: user.perfil
        verbose_name=_("usuário")
    )
    foto_perfil = models.ImageField(
        _("foto de perfil"),
        upload_to='usuarios/fotos_perfil/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text=_("Foto que será exibida no seu perfil.")
    )
    telefone = models.CharField(
        _("telefone"),
        max_length=20,
        blank=True,
        help_text=_("Telefone para contato, ex: (74) 99999-9999")
    )
    bio = models.TextField(
        _("biografia"),
        blank=True,
        help_text=_("Fale um pouco sobre você.")
    )

    class Meta:
        verbose_name = _("Perfil de Usuário")
        verbose_name_plural = _("Perfis de Usuários")

    def __str__(self):
        return f"Perfil de {self.usuario.username}"