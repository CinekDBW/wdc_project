from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .signals import populate_models


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):

        post_migrate.connect(populate_models, sender=self)
