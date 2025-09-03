
from django.contrib import admin
from catalog.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('id', )

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', )
    list_filter = ('category', 'created_at', 'changed_at', )
    search_fields = ('name', 'description', )
    ordering = ('-created_at', )
