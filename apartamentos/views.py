from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg
from django.forms import inlineformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View

from .services import aprovar_reserva_service, recusar_reserva_service
from .filters import ApartamentoFilter
from .models import Apartamento, Predio, Reserva, Avaliacao, FotoApartamento
from .forms import (
    CustomUserCreationForm, PredioForm, ApartamentoForm,
    UserUpdateForm, PerfilUpdateForm, ReservaForm, ApartamentoSearchForm,
    AvaliacaoForm
)


class HomePageView(TemplateView):
    template_name = 'homepage.html'


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def perfil_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        perfil_form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('apartamentos:perfil_edit')
    else:
        user_form = UserUpdateForm(instance=request.user)
        perfil_form = PerfilUpdateForm(instance=request.user.perfil)
    context = {'user_form': user_form, 'perfil_form': perfil_form}
    return render(request, 'apartamentos/perfil_edit.html', context)


# apartamentos/views.py
class ApartamentoListView(View):
    template_name = 'apartamentos/apartamento_list.html'

    def get(self, request, *args, **kwargs):
        base_queryset = Apartamento.objects.filter(disponivel=True).select_related('predio')

        filterset = ApartamentoFilter(request.GET, queryset=base_queryset)
        queryset_filtrado = filterset.qs

        # Lógica de filtro por data
        data_checkin_str = request.GET.get('data_checkin', '')
        data_checkout_str = request.GET.get('data_checkout', '')
        if data_checkin_str and data_checkout_str:
            # ... (a lógica de filtro de data continua a mesma, sem alterações) ...
            try:
                data_checkin = timezone.datetime.strptime(data_checkin_str, '%Y-%m-%d').date()
                data_checkout = timezone.datetime.strptime(data_checkout_str, '%Y-%m-%d').date()
                status_bloqueantes = [Reserva.StatusReserva.CONFIRMADA, Reserva.StatusReserva.PENDENTE]
                apartamentos_indisponiveis_ids = Reserva.objects.filter(
                    status__in=status_bloqueantes,
                    data_checkin__lte=data_checkout,
                    data_checkout__gte=data_checkin
                ).values_list('apartamento_id', flat=True)
                queryset_filtrado = queryset_filtrado.exclude(pk__in=apartamentos_indisponiveis_ids)
            except ValueError:
                pass

        # A consulta final, limpa e estável
        final_queryset = queryset_filtrado.distinct().order_by('-data_cadastro')

        # Paginação
        paginator = Paginator(final_queryset, 9)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            page_obj = paginator.page(1)

        # Contexto
        context = {
            'apartamentos': page_obj.object_list,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'filter': filterset,
            'cidades_disponiveis': Predio.objects.order_by('cidade').values_list('cidade', flat=True).distinct(),
            'is_search': bool(request.GET)
        }

        return render(request, self.template_name, context)

class PredioListView(ListView):
    model = Predio
    template_name = 'apartamentos/predio_list.html'
    context_object_name = 'predios'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        """
        Adiciona uma verificação explícita para o caso de a lista de prédios
        estar vazia, evitando o erro EmptyPage.
        """
        queryset = self.get_queryset()

        if not queryset.exists():
            # Se NÃO existir nenhum prédio, nós pulamos a lógica de paginação
            # e renderizamos o template com um contexto seguro.
            context = {'predios': []}
            return render(request, self.template_name, context)

        # Se EXISTEM prédios, deixamos o comportamento normal da ListView acontecer.
        return super().get(request, *args, **kwargs)

class PredioDetailView(DetailView):
    model = Predio
    template_name = 'apartamentos/predio_detail.html'
    context_object_name = 'predio'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('apartamentos__proprietario')


class ApartamentoDetailView(FormMixin, DetailView):
    model = Apartamento
    template_name = 'apartamentos/apartamento_detail.html'
    context_object_name = 'apartamento'
    form_class = ReservaForm

    def get_success_url(self):
        return reverse_lazy('apartamentos:minhas_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        # --- AQUI ESTÁ A MELHORIA ---
        status_bloqueantes = [Reserva.StatusReserva.CONFIRMADA, Reserva.StatusReserva.PENDENTE]

        # Adicionamos o filtro 'data_checkout__gte=timezone.localdate()'
        # gte = Greater Than or Equal (maior ou igual a)
        # Isso garante que só pegamos reservas que terminam hoje ou no futuro.
        context['datas_ocupadas'] = self.object.reservas.filter(
            status__in=status_bloqueantes,
            data_checkout__gte=timezone.localdate()
        ).order_by('data_checkin')
        # --- FIM DA MELHORIA ---

        # Lógica para buscar e exibir avaliações
        apartamento = self.get_object()
        avaliacoes = Avaliacao.objects.filter(reserva__apartamento=apartamento).order_by('-data_avaliacao')
        nota_media = avaliacoes.aggregate(Avg('nota'))['nota__avg']
        context['avaliacoes'] = avaliacoes
        context['nota_media'] = nota_media
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['apartamento'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        reserva = form.save(commit=False)
        reserva.apartamento = self.object
        reserva.hospede = self.request.user
        reserva.save()
        messages.success(self.request, "Sua solicitação de reserva foi enviada com sucesso!")
        return super().form_valid(form)

    def get_queryset(self):
        return super().get_queryset().select_related('predio', 'proprietario').prefetch_related('fotos', 'comodidades')


class ReservaDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Reserva
    template_name = 'apartamentos/reserva_detail.html'
    context_object_name = 'reserva'

    def test_func(self):
        reserva = self.get_object()
        return self.request.user == reserva.hospede or self.request.user == reserva.apartamento.proprietario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reserva = self.get_object()
        pode_avaliar = (
                reserva.status == Reserva.StatusReserva.CONFIRMADA and
                reserva.data_checkout < timezone.localdate() and
                self.request.user == reserva.hospede and
                not hasattr(reserva, 'avaliacao')
        )
        if pode_avaliar:
            context['form_avaliacao'] = AvaliacaoForm()
        return context

    def post(self, request, *args, **kwargs):
        reserva = self.get_object()
        # Apenas hóspedes podem postar avaliações
        if self.request.user != reserva.hospede:
            messages.error(request, "Você não tem permissão para avaliar esta reserva.")
            return redirect('apartamentos:detalhe_reserva', pk=reserva.pk)

        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.reserva = reserva
            avaliacao.save()
            messages.success(request, 'Sua avaliação foi enviada com sucesso. Obrigado!')
            return redirect('apartamentos:detalhe_reserva', pk=reserva.pk)

        context = self.get_context_data()
        context['form_avaliacao'] = form
        return self.render_to_response(context)

    def get_queryset(self):
        return super().get_queryset().select_related('hospede__perfil', 'apartamento__predio',
                                                     'apartamento__proprietario__perfil')


class PainelProprietarioView(PermissionRequiredMixin, TemplateView):
    template_name = 'apartamentos/painel_proprietario.html'
    permission_required = 'apartamentos.add_apartamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['predios'] = Predio.objects.filter(proprietario=user).prefetch_related('apartamentos')
        reservas = Reserva.objects.filter(apartamento__proprietario=user).select_related('hospede',
                                                                                         'apartamento').order_by(
            '-data_checkin')
        context['reservas_pendentes'] = reservas.filter(status=Reserva.StatusReserva.PENDENTE)
        context['reservas_confirmadas'] = reservas.filter(status=Reserva.StatusReserva.CONFIRMADA)
        context['historico_reservas'] = reservas.filter(status__in=[Reserva.StatusReserva.CANCELADA])
        context['titulo_pagina'] = "Painel do Proprietário"
        return context


class MinhasReservasListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'apartamentos/minhas_reservas.html'
    context_object_name = 'reservas'
    paginate_by = 10

    def get_queryset(self):
        return Reserva.objects.filter(hospede=self.request.user).select_related('apartamento__predio').order_by(
            '-data_checkin')


class PredioCreateView(PermissionRequiredMixin, CreateView):
    model = Predio
    form_class = PredioForm
    template_name = 'apartamentos/predio_form.html'
    permission_required = 'apartamentos.add_predio'

    def form_valid(self, form):
        form.instance.proprietario = self.request.user
        messages.success(self.request,
                         f"O prédio '{form.instance.nome}' foi cadastrado com sucesso! Agora adicione as unidades.")
        return super().form_valid(form)

    def get_success_url(self): return reverse_lazy('apartamentos:detalhe_predio', kwargs={'pk': self.object.pk})


class ApartamentoCreateView(PermissionRequiredMixin, CreateView):
    model = Apartamento
    form_class = ApartamentoForm
    template_name = 'apartamentos/apartamento_form.html'
    permission_required = 'apartamentos.add_apartamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['predio'] = get_object_or_404(Predio, pk=self.kwargs['pk_predio'])
        return context

    def form_valid(self, form):
        predio = get_object_or_404(Predio, pk=self.kwargs['pk_predio'])
        form.instance.predio = predio
        form.instance.proprietario = self.request.user
        return super().form_valid(form)

    def get_success_url(self): return reverse_lazy('apartamentos:detalhe_predio',
                                                   kwargs={'pk': self.kwargs['pk_predio']})


class ApartamentoUpdateView(PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Apartamento
    form_class = ApartamentoForm
    template_name = 'apartamentos/apartamento_form.html'
    permission_required = 'apartamentos.change_apartamento'

    def test_func(self): return self.request.user == self.get_object().proprietario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Cria a fábrica de formsets para o modelo FotoApartamento
        FotoFormSet = inlineformset_factory(
            Apartamento,
            FotoApartamento,
            fields=('imagem', 'principal'),
            extra=3, # Mostra 3 formulários extras para novas fotos
            can_delete=True # Permite deletar fotos existentes
        )
        if self.request.POST:
            context['formset'] = FotoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = FotoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, "Apartamento atualizado com sucesso!")
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self): return reverse_lazy('apartamentos:detalhe_apartamento', kwargs={'pk': self.object.pk})


class ApartamentoDeleteView(PermissionRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Apartamento
    template_name = 'apartamentos/apartamento_confirm_delete.html'
    context_object_name = 'apartamento'
    permission_required = 'apartamentos.delete_apartamento'

    def test_func(self): return self.request.user == self.get_object().proprietario

    def get_success_url(self): return reverse_lazy('apartamentos:painel_proprietario')

    def form_valid(self, form):
        messages.success(self.request, f"O anúncio '{self.object.titulo}' foi excluído com sucesso.")
        return super().form_valid(form)

# Adicione JsonResponse à esta linha de import
from django.http import HttpResponse, JsonResponse

@require_POST
@login_required
def aprovar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    try:
        # CORREÇÃO: Chamamos a função diretamente, sem o prefixo 'services.'
        aprovar_reserva_service(reserva=reserva, usuario=request.user)
        return JsonResponse({'status': 'success', 'message': 'Reserva aprovada com sucesso!'})
    except PermissionError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=403)


@require_POST
@login_required
def recusar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    try:
        # CORREÇÃO: Chamamos a função diretamente, sem o prefixo 'services.'
        recusar_reserva_service(reserva=reserva, usuario=request.user)
        return JsonResponse({'status': 'success', 'message': 'Reserva recusada.'})
    except PermissionError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=403)