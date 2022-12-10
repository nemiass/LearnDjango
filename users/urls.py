"""Users URLs."""

# Django
from django.urls import path
from django.views.generic import TemplateView

# Views
from users import views

urlpatterns = [
    # Posts
    # cuando solo vamos a mostrar un template y no aplcairemos mucha logica, para no etar estar 
    # haciendo su vista, simplemente usamos la calse generica que nos provee django TemplateView, y
    # le pasamos nuestro template y trabajamos, eso se usa en vistas donde no hay mucha logicas,
    # como una landing page por ejemplo
    # path(
    #     route="<str:username>/",
    #     view=TemplateView.as_view(template_name="users/detail.html"),
    #     name="detail"
    # ),

    # Management
    path(
        route="login/", 
        view=views.LoginView.as_view(), 
        name="login"
    ),
    path(
        route="logout/", 
        view=views.LogoutView.as_view(), 
        name="logout"
    ),
    path(
        route="signup/", 
        view=views.SignupView.as_view(), 
        name="signup"
    ),
    path(
        route="me/profile", 
        view=views.UpdateProfile.as_view(), 
        name="update"
    ),
    # Recordar que, este tipo de vostas debe estar siempre al ultimo para no confundir a la url
    # ya que este carga /users/algo, si ese algo es otra ruta, lo tomará como username, por
    # ello lo colocamos al ultimo en las prioridades, a menos que se cambia como se llama a la url
    path(
        # indicando que se va recibir el parametro username por la url
        route="<str:username>/",
        view=views.UserDetailView.as_view(),
        name="detail"
    ),
]
