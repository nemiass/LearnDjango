"""User forms."""

# Django
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import Profile

class ProfileForm(forms.Form):
    """Profile form."""

    website = forms.URLField(max_length=200, required=True)
    biography = forms.CharField(max_length=500, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    picture = forms.ImageField()


class SignupForm(forms.Form):
    # Nota: si no colocamos required como paramentro, este por defecto es True
    username = forms.CharField(min_length=4, max_length=50)
    # para agregar mas cosas a nuestro passwod, como por ejemplo que el input sea de tipo
    # password, osea "type='password'", para ello lo hacemos con el parametro widget,
    # y le pasamos forms.PasswordInput()
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(max_length=70, widget=forms.PasswordInput())
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)
    # A nuestro email tambien le pasamos un wodget, para indicar que el form
    # es de tipo EmailInput()
    email = forms.CharField(min_length=6, max_length=70, widget=forms.EmailInput())

    # Esto lo usamos para validar especificamente el username, anteponiendo el prefijo
    # clean_, seguido del nombre del campo
    def clean_username(self):
        """Username must be unique"""
        username = self.cleaned_data["username"]
        username_exists = User.objects.filter(username=username).exists()
        if username_exists:
            raise forms.ValidationError("Username is alredy in use.")
        return username

    # Si queremos validar cuando un campo depende del otro, tenemos que sobreescribir
    # el metodo clean
    def clean(self):
        """Verify password confirmation match."""
        # llamamos el al metodo clean con super(), para jalar los datos y no sobreescribir
        # rodo el metodos
        data = super().clean()
        password = data["password"]
        password_confirmation = data["password_confirmation"]
        # validamos si los passwords hacen match
        if password != password_confirmation:
            raise forms.ValidationError("Passwords do not match.")
        return data
    
    # Implementando su metodo save de nuestro formulario, ya que este no es un Form y 
    # no un ModelForm
    def save(self):
        # oteniendo los datos nuestro form
        data = self.cleaned_data
        # eliminamos password_confirmation de nuestro dicionario de data, ya que este
        # solo lo usamos para valida y no para guardar
        data.pop("password_confirmation")

        # creando a neustro usuario
        user = User.objects.create_user(**data)
        # creando un profile y asignandole el usuario, luego guardando el profile
        profile = Profile(user=user)
        profile.save()
