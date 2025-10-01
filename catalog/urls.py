from django.urls import path
from catalog.apps import CatalogConfig
from catalog import views as catalog_views

app_name = CatalogConfig.name

urlpatterns = [
    path('', catalog_views.HomeProductListView.as_view(), name='home'),
    path('product_list/', catalog_views.ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', catalog_views.ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', catalog_views.ContactsCreateView.as_view(), name='contacts'),
    path('contacts/success/', catalog_views.FeedBackMessageSent.as_view(), name='feedback_success'),
    path('products/create/', catalog_views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', catalog_views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', catalog_views.ProductDeleteView.as_view(), name='product_delete'),
    path('add_product/', catalog_views.ProductCreateView.as_view(), name='add_product'),
    path('products/<int:pk>/unpublish/', catalog_views.ProductUnpublishView.as_view(), name='product_unpublish'),
    path('category/<int:category_id>/', catalog_views.CategoryProductsView.as_view(), name='products_by_category'),
]



