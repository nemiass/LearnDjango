"""User models."""

# Django
from django.db import models
 #obteniendo el modelo User de Django para extender de el
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    """profile Model.

    Proxy model that extends the base data width other information.
    """

    # Haciendo la relacion one to one con el modelo User de django, con el objetivo de 
    # extender el modelo de usuario para añadirle mas propiedades
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(max_length=200, blank=True)
    biography = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    picture = models.ImageField(upload_to="users/pictures", blank=True, null=True)
    # columnas que se encargan de capturar la hora de creacion y modificación
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return username."""
        return self.user.username
