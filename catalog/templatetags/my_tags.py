from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_filter(value):
    """
    Возвращает корректный URL для ImageField/FileField или строкового пути.
    Пример: {{ product.pic|media_filter }}
    """
    if not value:
        return ''
    # Если это FileField/ImageField — у них есть .url
    url = getattr(value, 'url', None)
    if url:
        return url
    # Иначе считаем, что это строковый путь относительно MEDIA_ROOT
    path = str(value).lstrip('/')
    return settings.MEDIA_URL.rstrip('/') + '/' + path
