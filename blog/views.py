from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from.models import BlogPost



class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        BlogPost.objects.filter(pk=self.object.pk).update(views=F('views')+1)
        self.object.refresh_from_db(fields=['views'])
        return response


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog/blog_form.html'


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
