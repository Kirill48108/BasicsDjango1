from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product
from PIL import Image, UnidentifiedImageError


FORBIDDEN_WORDS_NAME = (
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар',
)
FORBIDDEN_WORDS_DESCRIPTION = (
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар',
)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'pic', 'category', 'price', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация через __init__
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите название продукта',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'rows': '5',
            'placeholder': 'Введите описание',
        })
        self.fields['pic'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Введите цену',
        })
        self.fields['is_published'].widget.attrs.update({
            'class': 'form-check-input',
        })

    def clean_name(self):
        name = (self.cleaned_data.get('name') or '').strip()
        lower = name.lower()
        if any(word in lower for word in FORBIDDEN_WORDS_NAME):
            raise ValidationError('Название содержит запрещенные слова.')
        return name

    def clean_description(self):
        description = (self.cleaned_data.get('description') or '').strip()
        lower = description.lower()
        if any(word in lower for word in FORBIDDEN_WORDS_DESCRIPTION):
            raise ValidationError('Описание содержит запрещенные слова.')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price < 0:
            raise ValidationError('Цена продукта не может быть отрицательной.')
        return price

    def clean_pic(self):

        file = self.cleaned_data.get('pic')
        if not file:
            return file

        max_size = 5 * 1024 * 1024  # 5 MB
        if getattr(file, 'size', 0) > max_size:
            raise ValidationError('Размер файла превышает 5 МБ.')


        try:
            pos = file.tell() if hasattr(file, 'tell') else None
            img = Image.open(file)
            img.verify()
            fmt = (img.format or '').upper()
        except (UnidentifiedImageError, OSError):
            raise ValidationError('Недопустимое изображение. Загрузите файл JPEG или PNG.')
        finally:
            try:
                if pos is not None:
                    file.seek(0)
            except Exception:
                pass

        if fmt not in ('JPEG', 'PNG'):
            raise ValidationError('Недопустимый формат. Разрешены только JPEG или PNG.')

        return file
