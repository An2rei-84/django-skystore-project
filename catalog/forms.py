from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from .models import Product, Feedback


from django.forms.widgets import CheckboxInput


class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования объектов модели Product с валидацией.
    """
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа', 'дешево',
        'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published']

    def __init__(self, *args, **kwargs):
        """
        Добавляет CSS-классы для стилизации полей формы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        name = self.cleaned_data.get('name', '').lower()
        for word in self.FORBIDDEN_WORDS:
            if word in name:
                raise ValidationError(f'Слово "{word}" запрещено в названии продукта.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '').lower()
        for word in self.FORBIDDEN_WORDS:
            if word in description:
                raise ValidationError(f'Слово "{word}" запрещено в описании продукта.')
        return description

    def clean_price(self):
        """
        Валидация цены: не должна быть отрицательной.
        """
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self):
        """
        Валидация изображения: формат JPEG/PNG и размер не более 5 МБ.
        Только для новых загруженных файлов.
        """
        image = self.cleaned_data.get('image')

        # Проверяем, является ли 'image' новым загруженным файлом.
        # Если это существующий файл (ImageFieldFile) или None, пропускаем валидацию.
        if isinstance(image, UploadedFile):
            # Проверка формата файла
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise ValidationError('Неверный формат файла. Допустимы только JPEG и PNG.')

            # Проверка размера файла (5 МБ)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5 МБ.')
        return image


class FeedbackForm(forms.ModelForm):
    """
    Форма для отправки сообщений обратной связи.
    """
    class Meta:
        model = Feedback
        fields = ['name', 'phone', 'message']

    def __init__(self, *args, **kwargs):
        """
        Добавляет CSS-классы для стилизации полей формы.
        """
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
