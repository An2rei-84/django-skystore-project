from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Административная панель для кастомной модели User.
    """
    # Указываем кастомные формы
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Определение полей для формы редактирования пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'avatar', 'phone_number', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Определение полей для формы создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'), # ИСПРАВЛЕНО!
        }),
    )
