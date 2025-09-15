from django.urls import path
from catalog.apps import CatalogConfig

from catalog.views import ProductListView, HomeProductListView, ProductDetailView, \
    ContactsCreateView, FeedBackMessageSent, AddProduct, ProductCreated

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeProductListView.as_view(), name='home'),
    path('product_list/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsCreateView.as_view(), name='contacts'),
    path('contacts/success/', FeedBackMessageSent.as_view(), name='feedback_success'),
    path('add_product/', AddProduct.as_view(), name='add_product'),
    path('product_created/', ProductCreated.as_view(), name='product_created'),
]
