from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.views.generic import UpdateView, DeleteView

from catalog.models import Product, FeedBackMessage
from catalog.forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

class ProductDetailView(DetailView):

    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:products')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('catalog:products')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products')
