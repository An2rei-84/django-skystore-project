from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from mailings.models import Mailing, Message, Client, Attempt
from mailings.forms import MailingForm, MessageForm, ClientForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required
def set_mailing_status(request, pk, status):
    """
    Контроллер для изменения статуса рассылки.
    Доступен только для владельца или пользователя с правом 'can_set_mailing_status'.
    """
    mailing = get_object_or_404(Mailing, pk=pk)

    # Проверяем права: либо владелец, либо менеджер с правом
    has_perm = request.user.has_perm('mailings.can_set_mailing_status')
    is_owner = mailing.owner == request.user

    if has_perm or is_owner:
        if status in [Mailing.STATUS_CREATED, Mailing.STATUS_STARTED, Mailing.STATUS_PAUSED, Mailing.STATUS_COMPLETED]:
            mailing.status = status
            mailing.save()

    return redirect('mailings:mailing_detail', pk=pk)


class OwnerMixin:
    """
    Миксин, который автоматически присваивает текущего пользователя
    в качестве владельца объекта при создании.
    """
    def form_valid(self, form):
        if not form.instance.owner_id:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class ManagerOrOwnerMixin(UserPassesTestMixin):
    """
    Миксин для проверки, является ли пользователь менеджером с соответствующими правами
    или владельцем объекта.
    """
    def test_func(self):
        user = self.request.user
        obj = self.get_object()

        # Для сообщений, проверяем владельца связанной рассылки
        owner = obj.mailing.owner if hasattr(obj, 'mailing') and hasattr(obj.mailing, 'owner') else getattr(obj, 'owner', None)

        # Формируем имя права доступа
        model_name = self.model._meta.model_name
        view_perm = f'mailings.view_any_{model_name}'

        is_owner = owner == user
        is_manager = user.has_perm(view_perm)

        return is_owner or is_manager


# Mailing CRUD
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailings.view_any_mailing'):
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


class MailingDetailView(LoginRequiredMixin, ManagerOrOwnerMixin, DetailView):
    model = Mailing
    template_name = 'mailings/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(LoginRequiredMixin, OwnerMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingUpdateView(LoginRequiredMixin, ManagerOrOwnerMixin, OwnerMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailings/mailing_form.html'
    success_url = reverse_lazy('mailings:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingDeleteView(LoginRequiredMixin, ManagerOrOwnerMixin, DeleteView):
    model = Mailing
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailings:mailing_list')


# Message CRUD
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailings.view_any_message'):
            return Message.objects.all()
        return Message.objects.filter(mailing__owner=user)


class MessageDetailView(LoginRequiredMixin, ManagerOrOwnerMixin, DetailView):
    model = Message
    template_name = 'mailings/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MessageUpdateView(LoginRequiredMixin, ManagerOrOwnerMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailings/message_form.html'
    success_url = reverse_lazy('mailings:message_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MessageDeleteView(LoginRequiredMixin, ManagerOrOwnerMixin, DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('mailings:message_list')


# Client CRUD
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'mailings/client_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailings.view_any_client'):
            return Client.objects.all()
        return Client.objects.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, ManagerOrOwnerMixin, DetailView):
    model = Client
    template_name = 'mailings/client_detail.html'
    context_object_name = 'client'


class ClientCreateView(LoginRequiredMixin, OwnerMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(LoginRequiredMixin, ManagerOrOwnerMixin, OwnerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailings/client_form.html'
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, ManagerOrOwnerMixin, DeleteView):
    model = Client
    template_name = 'mailings/client_confirm_delete.html'
    success_url = reverse_lazy('mailings:client_list')


# Attempt (Report) CRUD
class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'

    def get_queryset(self):
        user = self.request.user
        # Менеджеры с правом просмотра любых рассылок видят все попытки
        if user.has_perm('mailings.view_any_mailing'):
            return Attempt.objects.all().order_by('-timestamp')
        # Обычные пользователи видят попытки только своих рассылок
        return Attempt.objects.filter(mailing__owner=user).order_by('-timestamp')
