from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.conf import settings
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from catalog.models import Product, FeedBackMessage
from catalog.forms import ProductForm



class HomeProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()[:5]

class ContactsCreateView(CreateView):
    model = FeedBackMessage
    fields = ['name', 'phone', 'message']
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:feedback_success')

class FeedBackMessageSent(TemplateView):
    template_name = 'catalog/feedback_success.html'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # Низкоуровневое кеширование: учитываем страницу пагинации
        page = self.request.GET.get('page', '1')
        cache_key = f"products:list:page:{page}"
        qs = cache.get(cache_key)
        if qs is not None:
            return qs
        qs = super().get_queryset()
        cache.set(cache_key, qs, timeout=getattr(settings, 'CACHE_TTL', 300))
        return qs

# ... existing code ...

@method_decorator(cache_page(getattr(settings, 'CACHE_TTL', 300)), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        # ВАЖНО: назначаем владельца текущего пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        obj = self.get_object()
        # Редактировать может только владелец
        return obj.owner_id == self.request.user.id

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        # Удалять может владелец или любой пользователь с правом delete_product (модератор)
        return (obj.owner_id == user.id) or user.has_perm('catalog.delete_product')

# Доп. действие: отмена публикации — только при праве catalog.can_unpublish_product
class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('pk'))
        product.is_published = False
        product.save(update_fields=['is_published'])
        return redirect('catalog:product_detail', pk=product.pk)

# Представление для списка продуктов по категории (использует сервисную функцию)
class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        from catalog.services import get_products_by_category  # локальный импорт, чтобы избежать циклов
        category_id = self.kwargs.get('category_id')
        # можно добавить кэш и здесь, если нужно:
        cache_key = f"products:by_category:{category_id}:page:{self.request.GET.get('page','1')}"
        qs = cache.get(cache_key)
        if qs is not None:
            return qs
        qs = get_products_by_category(category_id=category_id)
        cache.set(cache_key, qs, timeout=getattr(settings, 'CACHE_TTL', 300))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category_id'] = self.kwargs.get('category_id')
        return ctx
