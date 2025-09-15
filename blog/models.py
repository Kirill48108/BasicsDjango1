from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """ Represents blog post """
    title = models.CharField(max_length=255,verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', null=True,blank=True,verbose_name='Изображение')
    is_published = models.BooleanField(default=False,verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0,verbose_name='Просмотры')
    created_at = models.DateTimeField(auto_now_add=True,verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Обновлено')


    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.pk])
