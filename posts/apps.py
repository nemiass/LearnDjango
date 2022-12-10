from django.apps import AppConfig

# Archivo de configuraciones de neustra App
class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "posts"
    # el verbode nama de nuestr aplicacion
    verbose_name = "Posts"
