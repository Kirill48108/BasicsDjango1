from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'(\+?\d{1,3})?[\d\s\-()]{7,20})$',
    message="Введите корректный номер телефона."
)


class User(AbstractUser):
    email = models.EmailField ('email address', unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True,null=True,verbose_name='Аватар')
    phone = models.CharField(max_length=20,validators=[phone_regex],blank=True,verbose_name='Телефон')
    country = models.CharField(max_length=100,blank=True,verbose_name='Страна')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email or self.username