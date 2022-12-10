"""Post forms."""
# Django
from django import forms

# Models
from posts.models import Posts

# en este caso extiendo de ModelForm y no de Form como ya vimos
class PostForm(forms.ModelForm):
    """Post model form."""

    class Meta:
        """Form settings."""
        # indicamos que usaremos nuestro modelo Posts para crear este ModelForm
        model = Posts
        # indicamos que campos usaremos del ModelForm
        fields = ("user", "profile", "title", "photo")