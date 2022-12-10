from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

# typing
from typing import Dict, Any

# forms
from posts.forms import PostForm

# models
from .models import Posts

# Create your views here.

# Con el decorador login required, hacemos que esta ruta esté accesible solo para usuario que hace login
#@login_required
# def list_posts(request: HttpRequest):
#     # listamos los pots y los ordenamos por "created", para hacerlo descendente le colocamos "-"
#     posts = Posts.objects.all().order_by("-created")
#     return render(request, "posts/feed.html", {"posts": posts})
class PostFeedView(LoginRequiredMixin, ListView):
    """Return all publish post"""
    # indicamos el nombre de nuestro template
    template_name = "posts/feed.html"
    # indicamos el nombre de nuestro modelo el cual se va listar
    model = Posts
    # indicamos que se va ordenar por "created" descendente con "-"
    ordering = ("-created", )
    # indicamos que va tener paginacion de 2
    paginate_by = 2
    # indicamos el nombre del objeto contexto que se va pasar al template
    context_object_name = "posts"

class PostDetailView(LoginRequiredMixin, DetailView):
    """Return post detail."""
    # indicamos el template
    template_name = "posts/detail.html"
    # indicamos el query set del cual se va sacar el dato, el dato será un post especifico
    queryset = Posts.objects.all()
    # indicamos el nombre del context name, el nombre del contexto
    context_object_name = "post"
    # En este caso, el slug_url_kwarg no lo hemos defino tampoco el slug_field, en este
    # caso los toma por defecto el nombre que se le está pasando por la url, el nombre
    # es pk, por ello el DetailView intuye que va buscar un post de acuerdo a su fk,
    # ademas solo tenemos una relacion y eso lo facilita

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post."""
    template_name = "posts/new.html"
    # indicando el modelo de formulario
    form_class = PostForm
    # con reverse lazy indicamos la url cuando el usuario se registra exitosamente, lazy
    # porque solo se evaluará cuando lo necesitemos
    success_url = reverse_lazy("posts:feed")

    # Añadiendo mas datos al contexto ya que necesitaremos mas datos, esto lo hacemos
    # sobreescribiendo el get_context_data
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        return context


# @login_required
# def create_post(request: HttpRequest):
#     """Create new post view."""
#     if request.method == "POST":
#         # pasando el POST y los FILES, ya que en este caso tenemos files por guardar
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Con el ModelForm, tenemos la ventaja de hacer esto, ya que este usa nustro
#             # modelo de Posts
#             form.save()
#             return redirect("posts:feed")
#     else:
#         form = PostForm()
    
#     return render(
#         request=request,
#         template_name="posts/new.html",
#         context= {
#             "form": form,
#             "user": request.user,
#             "profile": request.user.profile
#         }
#     )
