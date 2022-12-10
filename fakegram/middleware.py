""" Platzigram middleware catalog."""
#Django
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    """Profile completion middleware.
    
    Ensure every user that is interacting with the platform
    have their profile picture and biography.
    """

    def __init__(self, get_response):
        """Middleware initialization."""
        self.get_response = get_response
    
    # Funcion principal de nuestro moddleware
    def __call__(self, request: HttpRequest):
        """Code to be executed for each request before the view is called."""
        # validamos que el usuario no sea anonimo, o sea este middleware solo será para 
        # usuarios autenticados
        if not request.user.is_anonymous:
            # Aplicamos la logica de redireccion si el usuario no es staff, si este es
            # staff queremos que pueda acceder a su login de admin normalmente
            if not request.user.is_staff:
                # Obtenemos el profile de nuestro usuario, ya que sabemos que estan relacionados
                profile = request.user.profile
                # validamos que tenga un picture o una biograpy, si no los tiene lo redireccionamos
                # al update profile
                if not profile.picture or not profile.biography:
                    # hacemos que redirija a update_profile siempte y cuando no sea la misma
                    # ruta ni tampoco sea el logout, ya que queremos no aplicar el middleware en estos
                    if request.path not in [reverse("users:update"), reverse("users:logout")]:
                        return redirect("users:update")
        
        response = self.get_response(request)
        return response

