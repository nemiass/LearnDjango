"""fakegram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from fakegram import views as local_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/', local_views.hello_world, name="hello_world"),
    path('sorted/', local_views.sort_integers, name="sort"),
    path('hi/<str:name>/<int:age>/', local_views.say_hi, name="hi"),

    # con include incuimos los urls de las otras apps, con el namespace le asiganmos un name
    # a ese grupo de urls
    path("", include(("posts.urls", "posts"), namespace="posts")),
    path("users/", include(("users.urls", "users"), namespace="users"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Para poder ver archivos estaticos(imagenes, etc) en django admin, al url patterns principal
# del proyecto al array le sumamos static que viene de django.conf.urls.statis y en ella
# le metemos la Media URL, el cual es la ruta que va llevar el navegador, y tambien el
# document ROOT, el cual es la ruta raiz de la imagen dentro del server y proyecto
# En resumen, el static, le suma al "urlpatterns" una url estatica con la variable MEDIA_URL
# y tambien donde estamos parados en la media, que es el MEDIA_ROOT

# Dentro de "settings" debemos configurar esas variables MEDIA_URL Y MEDIA_ROOT
