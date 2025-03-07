from django.apps import AppConfig


class PawAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paw_auth'

class ServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server'
