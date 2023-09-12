from django.apps import AppConfig

__all__ = (
    'Config',
)


class Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Posts'
