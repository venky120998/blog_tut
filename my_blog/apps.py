from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_blog'
    def ready(self):
        from my_blog.signals import create_groups_permissions
        post_migrate.connect(create_groups_permissions)