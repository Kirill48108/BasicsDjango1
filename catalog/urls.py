from django.urls import path
from catalog.apps import CatalogConfig

from catalog.views import ProductListView, HomeProductListView, ProductDetailView, \
    ContactsCreateView, FeedBackMessageSent, ProductCreateView, ProductUpdateView, ProductDeleteView,ProductUnpublishView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeProductListView.as_view(), name='home'),
    path('product_list/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactsCreateView.as_view(), name='contacts'),
    path('contacts/success/', FeedBackMessageSent.as_view(), name='feedback_success'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),

]
