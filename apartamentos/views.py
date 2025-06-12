# apartamentos/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Apartamento, Predio
from .forms import CustomUserCreationForm, PredioForm, ApartamentoForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

class PredioListView(ListView):
    """ View para listar todos os prédios/condomínios. """
    model = Predio
    template_name = 'apartamentos/predio_list.html'
    context_object_name = 'predios'
    paginate_by = 10

class PredioDetailView(DetailView):
    """ View para exibir os detalhes de um prédio e seus apartamentos. """
    model = Predio
    template_name = 'apartamentos/predio_detail.html'
    context_object_name = 'predio'

    def get_queryset(self):
        # Otimização: pré-carrega os apartamentos e suas respectivas fotos principais e proprietários
        return super().get_queryset().prefetch_related(
            'apartamentos__foto_principal',
            'apartamentos__proprietario'
        )

class ApartamentoListView(ListView):
    """ View para listar todos os apartamentos de todos os prédios. """
    model = Apartamento
    template_name = 'apartamentos/apartamento_list.html'
    context_object_name = 'apartamentos'
    paginate_by = 9

    def get_queryset(self):
        # Otimização: agora precisamos também dos dados do prédio
        return super().get_queryset().filter(disponivel=True).select_related('predio', 'proprietario')

class ApartamentoDetailView(DetailView):
    """ View para exibir os detalhes de um único apartamento. """
    model = Apartamento
    template_name = 'apartamentos/apartamento_detail.html'
    context_object_name = 'apartamento'

    def get_queryset(self):
        # Otimização: prédio, proprietário, fotos e comodidades
        return super().get_queryset().select_related('predio', 'proprietario').prefetch_related('fotos', 'comodidades')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    # reverse_lazy() é usado aqui porque as URLs só são carregadas quando o
    # servidor está rodando, e não quando o arquivo é importado.
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Página de Perfil do Usuário
@login_required # Este decorator garante que apenas usuários logados acessem esta view
def perfil_view(request):
    # O objeto do usuário logado já está disponível em 'request.user'
    # O perfil relacionado é acessado via 'request.user.perfil'
    template_name = 'apartamentos/perfil.html'
    context = {
        'usuario': request.user
    }
    return render(request, template_name, context)

# Painel "Meus Anúncios"
class MeusAnunciosListView(LoginRequiredMixin, ListView):
    model = Apartamento
    template_name = 'apartamentos/meus_anuncios.html'
    context_object_name = 'apartamentos'

    def get_queryset(self):
        # Filtra os apartamentos para mostrar apenas os que pertencem ao usuário logado
        return Apartamento.objects.filter(proprietario=self.request.user).order_by('-data_cadastro')

# Criar um novo Prédio
class PredioCreateView(LoginRequiredMixin, CreateView):
    model = Predio
    form_class = PredioForm
    template_name = 'apartamentos/predio_form.html'
    success_url = reverse_lazy('apartamentos:lista_predios') # Vamos ajustar isso depois

    def form_valid(self, form):
        # AQUI definimos o proprietário do prédio como o usuário logado
        # ANTES do formulário ser salvo.
        # form.instance.proprietario = self.request.user # Descomente quando adicionar 'proprietario' ao modelo Predio
        return super().form_valid(form)

# Criar um novo Apartamento em um Prédio específico
class ApartamentoCreateView(LoginRequiredMixin, CreateView):
    model = Apartamento
    form_class = ApartamentoForm
    template_name = 'apartamentos/apartamento_form.html'

    def get_context_data(self, **kwargs):
        # Adiciona o objeto do prédio ao contexto do template
        context = super().get_context_data(**kwargs)
        context['predio'] = get_object_or_404(Predio, pk=self.kwargs['pk_predio'])
        return context

    def form_valid(self, form):
        # Pega o prédio da URL
        predio = get_object_or_404(Predio, pk=self.kwargs['pk_predio'])
        # Associa o apartamento a esse prédio e ao usuário logado
        form.instance.predio = predio
        form.instance.proprietario = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redireciona para a página de detalhes do prédio após criar o apartamento
        return reverse_lazy('apartamentos:detalhe_predio', kwargs={'pk': self.kwargs['pk_predio']})

# Editar um Apartamento existente
class ApartamentoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Apartamento
    form_class = ApartamentoForm
    template_name = 'apartamentos/apartamento_form.html'

    def test_func(self):
        # Lógica de permissão: o usuário logado deve ser o proprietário do apartamento
        apartamento = self.get_object()
        return self.request.user == apartamento.proprietario

    def get_success_url(self):
        # Redireciona para a página de detalhes do apartamento após a edição
        return reverse_lazy('apartamentos:detalhe_apartamento', kwargs={'pk': self.object.pk})