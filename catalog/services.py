from catalog.models import Product

def get_products_by_category(category_id: int):
    """Возвращает QuerySet всех продуктов указанной категории (опубликованные)."""
    return Product.objects.filter(category_id=category_id, is_published=True).order_by('-created_at')
