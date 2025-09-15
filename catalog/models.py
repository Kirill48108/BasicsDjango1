
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import TextField





# Create your models here.
class Category(models.Model):
    """ Represents category """
    name = models.CharField(max_length=150, verbose_name='Category name')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']


class Product(models.Model):
    """ Represents product """
    name = models.CharField(max_length=150, verbose_name='Product name')
    description = models.TextField(verbose_name='Description')
    pic = models.ImageField(upload_to='photos/', verbose_name='Photo')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')
    changed_at = models.DateTimeField(auto_now=True, verbose_name='Time of changing')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-created_at']

    # Validator
phone_regex = RegexValidator(
    regex=r'^(\+?\d{1,3})?(\d{10})$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
class FeedBackMessage(models.Model):
    """ Represents Feedback Message """
    name = models.CharField(max_length=150, verbose_name='Name')
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name='Phone number')
    message = TextField(verbose_name='Message', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Time of creation')