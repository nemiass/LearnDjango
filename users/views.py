"""Users views."""

# Django
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import views as auth_views

# types
from typing import Dict, Any
from django.db import models

# Models
from django.contrib.auth.models import User
from users.models import Profile
from posts.models import Posts

# Exceptions
from django.db.utils import IntegrityError
from django.views.generic import DetailView, FormView, UpdateView

#Importando nuestros formualrios creados con Forms de django
from users.forms import ProfileForm, SignupForm

# Create your views here.

# Creamos la clase UserDetailView, este geredará de LoginRequiredMixin para verificar que
# este se acceda cuanel usuairo esté logueado, y tambien heredamos de DetailView para personalizar
# nuestra clase y agregrle mas logica 
class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view"""
    # indicamos el nombre del template
    template_name = "users/detail.html"
    # indicamos el nombre del parametro que va recibir de la url, en este caso va ser username
    # ya que así lo configuramos en el views de users
    slug_url_kwarg = "username"
    # en este caso indicamos el slug_fiels por el cual se va buscar algo, 
    # en este caso se buscará de la lista de usuarios por el username, todo esto del queryset
    slug_field = "username"
    # indicamos el queryset, el cual va ser por el por el que va obtener un usuario, de acuerdo
    # a su username que indicamos en el slug_field
    queryset = User.objects.all()
    # indicamos el nombre que le daremos al objeto encontrado del query set, en este caso será
    # el contexto con el nombre de user, este se accederá desde el template detail
    context_object_name = "user"

    # si queremos pasar mas datos a nuestro template, podemos hacerlo sobreescribiendo el
    # metodo get_context_data de DetailView
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # obtenemos el contex data de nuestro padre DetailView
        context = super().get_context_data(**kwargs)
        # Obtenemos al user que se obtuvo gracias al queryset y el slug_fiel que le indicamos,
        # con el metodo get_object() obtenemos el objeto que se filtró del query set
        user = self.get_object()
        # agregamos "posts" a nuestro context para usarlo en el template, de esta forma
        # podemos agregar mas cosas al context
        context["posts"] = Posts.objects.filter(user=user).order_by("-created")
        return context

class SignupView(FormView):
    """Users signup view"""
    # indicamos el template
    template_name = "users/signup.html"
    # indicamos el form
    form_class = SignupForm
    # indicamos la redireccion en caso de que sea success, con lazy para que cargue solo cuando
    # lo necesitamos
    success_url = reverse_lazy("users:login")

    # Para poder registrar en ese caso de Form, debemos sobreescibir su metodo form_valid
    # y luego ahí recien hacemos uso del form, y ejecutamos su metodo save que definimos,
    # luego de ello redireccionamos normalnte par aque continua haceindo lo que hacia form_valid
    def form_valid(self, form ) -> HttpResponse:
        # registrando al user con el form
        form.save()
        return super().form_valid(form)
     
# def signup_view(request: HttpRequest):
#     "Signup view."
#     # import pdb; pdb.set_trace() # debugueando, esto podemo accdeder desde la terminal
#     if request.method == "POST":
#         # instanciamos nuestro Form
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             # Ejecutamos el metodo save que creamos
#             form.save()
#             return redirect("users:login")
#     else:
#         form = SignupForm()
#     return render(
#         request=request,
#         template_name="users/signup.html",
#         context= {
#             "form": form
#         }
#     )

class UpdateProfile(LoginRequiredMixin, UpdateView):
    """Update profile view."""
    # indicamos el template
    template_name = "users/update_profile.html"
    # indicamos el modelo a actualizar
    model = Profile
    # indicamos los atributos el cuales se van a actualizar, recordar que este debe
    # hacer match con el formulario de actualziacion y el modelo
    fields = ["website", "biography", "phone_number", "picture"]

    # sobreescribimo el metodo get_object, para indicar el objecto con el cual va trabajar,
    # en este caso va sel el profile, y este se encuantra en request.user.profile
    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    # sobreescribimos el metodo get_success_url para indicar cual va ser el url de 
    # redireccion, como sabes es una url que le debemos pasar un username por 
    # parametro, entonces esto lo construimos
    def get_success_url(self) -> str:
        """Return to user's profile."""
        username = self.object.user.username
        return reverse("users:detail", kwargs={"username": username})

# @login_required
# def update_profile(request: HttpRequest):
#     """Update a user's profile view."""
#     profile = request.user.profile
#     if request.method == "POST":
#         # Si el post, instanciamos nuestro Form, y este le pasamos nuestro request.POST,
#         # si vamos a pasar un archivo, le pasamos request.FILES ya que los archivos 
#         # se guardan en FILES del request.
#         form = ProfileForm(request.POST, request.FILES)
#         # Comprobamos que el formulario sea valido
#         if form.is_valid():
#             # si este es valido, tomamos los datos con "cleaned_data" y los seteamos a profiles
#             data = form.cleaned_data
#             profile.website = data["website"]
#             profile.biography = data["biography"]
#             profile.phone_number = data["phone_number"]
#             profile.picture = data["picture"]
#             profile.save()
#             # pasando argumentos a la url, ya que este los requiere, para eso necesitamos
#             # usar reverse() de django, ya que con redirect no se puede
#             url = reverse("users:detail", kwargs={"username": request.user.username})
#             return redirect(url)
#     else:
#         # si no es post instanciamos un form vacío
#         form = ProfileForm()
#     # agregando contexto al render
#     # Tambien, le pasamos el "form" en nuestro context

#     return render(
#         request,
#         template_name="users/update_profile.html",
#         context={"profile": profile, "user": request.user, "form": form},
#     )


class LoginView(auth_views.LoginView):
    """Login view."""
    template_name = "users/login.html"


# def login_view(request):
#     """Login view."""
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         # usando authenticate para validar a nuestro usuario
#         user = authenticate(request, username=username, password=password)
#         if user:
#             # si el user no es nulo, se crea la sesións, luego lo redirige al feed
#             login(request, user)
#             # regireccionamos y usamos el nombre de nuestra ruta, en este caso feed
#             return redirect("posts:feed")
#         else:
#             return render(
#                 request, "users/login.html", {"error": "Invalid username and password"}
#             )
#     return render(request, "users/login.html")


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""
    # colocar este template no es necesario, pero lo colocamos como ejemplo
    template_name = "users/logged_out.html"


# @login_required
# def logout_view(request):
#     """Logout a user."""
#     logout(request)
#     return redirect("users:login")


