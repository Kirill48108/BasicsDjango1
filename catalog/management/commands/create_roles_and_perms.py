from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from catalog.models import Product
from blog.models import BlogPost


class Command(BaseCommand):
    help = 'Создаёт группы ролей и назначает необходимые разрешения'

    def handle(self, *args, **options):
        # Группа "Модератор продуктов"
        product_moderator_group, _ = Group.objects.get_or_create(name='Модератор продуктов')

        product_ct = ContentType.objects.get_for_model(Product)
        perms_to_assign = []

        # Кастомное право на отмену публикации продукта
        try:
            can_unpublish = Permission.objects.get(
                content_type=product_ct,
                codename='can_unpublish_product'
            )
            perms_to_assign.append(can_unpublish)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.WARNING('Право can_unpublish_product не найдено. Убедитесь, что выполнены миграции.'))

        # Право на удаление любого продукта (стандартное)
        try:
            delete_product = Permission.objects.get(
                content_type=product_ct,
                codename='delete_product'
            )
            perms_to_assign.append(delete_product)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.WARNING('Право delete_product не найдено. Убедитесь, что выполнены миграции.'))

        product_moderator_group.permissions.set(list({p.id: p for p in perms_to_assign}.values()))
        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" настроена.'))

        # Группа "Контент-менеджер" (для блога)
        content_manager_group, _ = Group.objects.get_or_create(name='Контент-менеджер')
        blog_ct = ContentType.objects.get_for_model(BlogPost)
        blog_perms = Permission.objects.filter(
            content_type=blog_ct,
            codename__in=['add_blogpost', 'change_blogpost', 'delete_blogpost']
        )
        content_manager_group.permissions.set(blog_perms)
        self.stdout.write(self.style.SUCCESS('Группа "Контент-менеджер" настроена.'))
