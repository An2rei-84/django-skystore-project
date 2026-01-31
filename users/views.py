from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm
from users.models import User
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Поздравляем с регистрацией!',
            message='Вы успешно зарегистрировались на нашем сайте!',
            from_email=None,  # будет использован DEFAULT_FROM_EMAIL
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user