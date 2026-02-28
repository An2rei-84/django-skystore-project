"""
Конфигурация URL для основного проекта.

Список `urlpatterns` направляет URL-адреса на представления. Для получения дополнительной информации смотрите:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Примеры:
Представления-функции (Function views)
    1. Добавьте импорт:  from my_app import views
    2. Добавьте URL в urlpatterns:  path('', views.home, name='home')
Представления-классы (Class-based views)
    1. Добавьте импорт:  from other_app.views import Home
    2. Добавьте URL в urlpatterns:  path('', Home.as_view(), name='home')
Включение другого файла URLconf
    1. Импортируйте функцию include(): from django.urls import include, path
    2. Добавьте URL в urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),  # Маршруты административной панели Django
    path('', include('catalog.urls')),  # Включение URL-маршрутов приложения каталога
    path('blogs/', include('blog.urls')),  # Включение URL-маршрутов приложения блога
    path('mailings/', include('mailings.urls', namespace='mailings')),
    path('users/', include('users.urls', namespace='users')),  # Включение URL-маршрутов приложения пользователей
]

# Добавление маршрутов для медиа-файлов в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
