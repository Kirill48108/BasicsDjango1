from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Product

from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import forms

def product_list(request):
    """ Page with all products """
    product_list = Product.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(product_list, 10)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, pk):
    """ Product detail page """
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)

def home(request):
    """ Home page with 5 latest products """
    latest_products = Product.objects.order_by('-created_at')[:5]
    context = {
        'products': latest_products
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    """ Page with contact info """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Thanks, {name}! Message received.')
    return render(request, 'catalog/contacts.html')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'pic', 'price', 'category']

def add_product(request):
    """ Page with add product form """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:products')
    else:
        form = ProductForm()
    return render(request, 'catalog/add_product.html', {'form': form})

