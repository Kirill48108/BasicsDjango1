from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView

from catalog.models import Product, FeedBackMessage


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetailView(DetailView):
    """ Product detail page """
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
    """ Page for Contacts with Feedback message feature """
    model = FeedBackMessage
    fields = ['name', 'phone', 'message']
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:feedback_success')


class FeedBackMessageSent(TemplateView):
    template_name = 'catalog/feedback_success.html'


class AddProduct(CreateView):
    model = Product
    fields = ['name', 'description', 'pic', 'price']
    template_name = 'catalog/add_product.html'
    success_url = reverse_lazy('catalog:product_created')

class ProductCreated(TemplateView):
    template_name = 'catalog/product_created.html'