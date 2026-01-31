from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'country', 'phone_number', 'avatar',)


class CustomUserCreationForm(UserCreationForm):
    """Кастомная форма создания пользователя для админки."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2') # ИСПРАВЛЕНО! Использование password1 и password2



class CustomUserChangeForm(UserChangeForm):
    """Кастомная форма изменения пользователя для админки."""
    class Meta:
        model = User
        fields = '__all__' # Исправлено: используем все поля, видимость контролируется через Admin


class CustomAuthenticationForm(AuthenticationForm):
    """
    Кастомная форма аутентификации, использующая email вместо username.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите email'})
