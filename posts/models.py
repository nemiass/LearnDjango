"""Posts Models"""

# Django
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# TODO: cambiar nombre del modelo Posts a Post
class Posts(models.Model):
    """Post Models"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # "users.Profile" es otra forma de hacer referencia al modelo Profile de el app users, esta es
    # una forma sin hacer importaciones, esto puede evitar referencias circulares
    profile = models.ForeignKey("users.Profile", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="posts/photos")

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return title and Username"""
        return f"{self.title} by {self.user.username}"

# class User(models.Model):

#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)

#     is_admin = models.BooleanField(default=False)

#     bio = models.TextField()
#     # acepta que un capo sea blank y se coloca nulo
#     birthdate = models.DateField(blank=True, null=True)

#     # auto_now_add hace que la fecja se agregue automaticamente
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

