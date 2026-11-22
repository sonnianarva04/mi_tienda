from django.contrib import messages                                  # mensajes
from django.contrib.auth import login, logout                      # abrir y cerrar sesión
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Sum                                   # SUM() de SQL
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView                      # NUEVO: VBC que muestra un template

from facturacion.models import Producto, Venta                     # NUEVO: para los números del inicio



# ---------------------------------------------------------------
# 1) HttpResponse: devuelve un texto o HTML escrito aquí mismo.
#    Sirve para pruebas rápidas. No se usa para páginas grandes.
# ---------------------------------------------------------------
def saludo(request):                                   # Toda vista recibe request
    return HttpResponse("<h1>¡Hola desde Django!</h1><p>Esto es un HttpResponse.</p>")  # Respuesta: ese HTML


# ---------------------------------------------------------------
# 2) JsonResponse: devuelve DATOS en formato JSON (no una página).
#    Lo usan las apps móviles y JavaScript para pedir información.
#    Recibe un diccionario de Python y lo convierte en JSON.
# ---------------------------------------------------------------
def info_peticion(request):
    datos = {                                          # Armamos un diccionario con datos de la petición
        "metodo": request.method,                      # 'GET' o 'POST'
        "ruta": request.path,                          # la dirección visitada, por ejemplo '/info/'
        "parametros_get": request.GET.dict(),          # lo que viene después del ? en la URL
        "navegador": request.headers.get("User-Agent", ""),  # qué navegador usa la persona
    }
    return JsonResponse(datos)                         # Lo devolvemos como JSON
    # Para devolver una LISTA en vez de un diccionario: JsonResponse([1, 2, 3], safe=False)


# ---------------------------------------------------------------
# 3) render: junta un TEMPLATE (.html) con un CONTEXTO (diccionario de datos)
#    y devuelve la página terminada. Es lo que usarás casi siempre.
#    Forma: render(request, "nombre_del_template.html", contexto)
# ---------------------------------------------------------------
def home(request):
    nombre = "nombre primera vez:get"                                        # Empieza vacío

    # ¿Cómo llegó la petición? Esta pregunta es la clave de todo el curso:
    if request.method == "POST":                       # Si llegó por POST (el usuario envió el formulario)...
        nombre = request.POST.get("nombre", "").strip()   # ...leemos el campo name="nombre" (strip quita espacios)
    # Si llegó por GET (solo abrió la página), no hacemos nada especial.

    contexto = {                                       # Datos que vamos a enviar al template
        "titulo": "Mi Tienda",                         # En el HTML se usa como {{ titulo }}
        "nombre": nombre,                              # En el HTML se usa como {{ nombre }}
        "productos": ["Laptop", "Mouse", "Teclado","Pendrive","Disco duro"],   # Una lista para practicar el {% for %}
    }
    print("metodo que viaja=",request.method)
    return render(request, "home.html", contexto)      # Junta home.html + contexto y responde

# =====================================================================
# INICIO · tu primera Vista Basada en Clases
# =====================================================================
class InicioView(TemplateView):                    # TemplateView: "muestra un template con datos"
    template_name = "home.html"                    # ATRIBUTO: ¿qué HTML?

    def get_context_data(self, **kwargs):          # MÉTODO: ¿qué datos recibe el HTML?
        contexto = super().get_context_data(**kwargs)   # 1. lo que TemplateView ya prepara
        hoy = timezone.localdate()                      # 2. la fecha de hoy en Ecuador
        ventas_hoy = Venta.objects.filter(fecha_hora__date=hoy)
        contexto["total_productos"] = Producto.objects.filter(activo=True).count()
        contexto["ventas_hoy"] = ventas_hoy.count()
        contexto["vendido_hoy"] = ventas_hoy.aggregate(suma=Sum("total"))["suma"] or 0   # SUM(total)
        contexto["stock_bajo"] = Producto.objects.filter(activo=True, stock__lt=5)        # menos de 5 unidades
        return contexto                                 # 3. entregamos todo


# =====================================================================
# AUTENTICACIÓN · se queda en funciones (VBF), como en la guía anterior
# =====================================================================

def ingresar(request):                                     # LOGIN
    if request.user.is_authenticated:                      # ya inició sesión → al inicio
        return redirect("home")
    siguiente = request.POST.get("next") or request.GET.get("next") or ""   # la página que quería ver
    if request.method == "POST":                           # presionó "Ingresar"
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():                                # usuario y clave correctos
            login(request, form.get_user())                # abre la sesión
            if siguiente and url_has_allowed_host_and_scheme(siguiente, allowed_hosts={request.get_host()}):
                return redirect(siguiente)
            return redirect("home")
    else:                                                  # GET: formulario vacío
        form = AuthenticationForm(request)
    return render(request, "registration/login.html", {"form": form, "next": siguiente})


@require_POST                                              # cerrar sesión SOLO con POST
def salir(request):                                        # LOGOUT
    logout(request)
    messages.info(request, "Cerraste sesión.")
    return redirect("login")


def registro(request):                                     # CREAR CUENTA
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()                          # crea el usuario con la clave cifrada
            login(request, usuario)
            messages.success(request, f"¡Bienvenido, {usuario.username}!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/registro.html", {"form": form})