# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

#improtando nuestro modelo de usuarrio
from users.models import Profile
from django.contrib.auth.models import User

# Register your models here.
# admin.site.register(Profile)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin"""
    #Configurando que queremos ver cuando listamos los profiles en el panel adminsitradivo de django
    list_display = ('pk', 'user', 'phone_number', 'website', 'picture')
    #con list_display_links, indicamos que campos queremos que sean cliqueables cuando se listan en 
    # el panel del admin, osea que campos queremos que nos redirija al nustro modelo profile dentro
    # django admin. Nota: "pk" hace referencia a la llave foranea de nustro profile
    list_display_links = ('pk', 'user')
    # con list editable, hacemos que el campo sea editable cuando se lista en el panel de admin de django
    # cuando un campo está en list_editable, no puede estar list_display_links
    list_editable = ('phone_number', 'website', 'picture')
    # Agregando filtro de busqueda, como user es una relacion, se debe colocar al user__ con
    # doble huión bajo para llamar a sus propiedades, aca se añaden los campos por el cual
    # queremos que se busque
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    # Agregando filtros, en este caso colocamos created y modified a estos django los entiende que son
    # el created_at y modified_at, en si aca podemos colocar todos los campos que queremos que sean filtros
    # el orden en que aparecen estos filtros dependen del orden en quelos colocamos
    list_filter = ('user__is_active', 'user__is_staff', 'created', 'modified')

    # COnifgurando el detalle de perfil, osea cunado hacemos click en el perfil nos lleva al detalle.
    # En este caso lo hacemos con fieldsets, recibe un tupla, llena de tuplas, esas tuplas tiene un
    # titulo, en este caso sirve para agruparlos como por ejemplo "Profile", luego del titulo colocamos
    # un diccionario que lleva la llave "fields" y este lleva una tupla de las filas que agruparemos,
    # si a esta tupla le metemos otra tupla se agtupará de manera horizontal
    fieldsets = (
        ('Profile', {
            'fields': (('user', 'picture'),)
        }),
        ('Extra Info', {
            'fields': (('website', 'phone_number'), ('biography'))
        }),
        # En este caso, el created y el modified, dan errores porque no se pueden editar, para ese
        # caso los ponemos en el "readonly_fields", para que solo se puedan leer y no editar
        ('Metadata', {
            'fields': (('created', 'modified'), )
        })
    )
    # En el readonly_fields se colocan los campos que queremos que solo sean de lectura y no de edicion
    readonly_fields = ('created', 'modified', 'user')

# La documentacion nos dice que creamos este modelo llamado ProfileInline y le ponemos los sigueintes
# atributos
class ProfileInline(admin.StackedInline):
    """Profile in-line admin for users."""
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"
# Luego del modelo ProfileInline creamos nustro UserAdmin, que hereda de BaseUserAdmin
# que es el UserAdmin, osea no heredea de admin.ModelAdmin como sería normalmente, luego le
# agregamos la propeidad inlines en el cual colocamos una tupla donde ponemos a la clase ProfileInline 
class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin"""
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
# Ahora lo que tenemos que hacer es, desregistrar el modelo User del admin site,
# y lo volvemos a registrar al modelo User y tambien pasamos nuestro UserAdmin, UserAdmin ya se
# encuntra linkeado con nuestro Profile
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# con tdo esto, cuando agreguemos un usaurio en el panel de django, al mismo tiempo
# podemos agregarle su perfil
