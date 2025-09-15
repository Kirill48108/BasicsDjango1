from django.urls import path


from .views import (
    BlogPostListView,
    BlogPostCreateView,
    BlogPostDetailView,
    BlogPostUpdateView,
    BlogPostDeleteView
)


app_name = 'blog'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('create/', BlogPostCreateView.as_view(), name='blog_create'),
    path('<int:pk>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),
]