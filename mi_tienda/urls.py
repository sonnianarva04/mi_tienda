"""
URL configuration for mi_tienda project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.InicioView.as_view(), name="home"),          # VBC: .as_view() convierte la clase en vista
    # ---------- AUTENTICACIÓN: funciones (VBF) ----------
    path("login/", views.ingresar, name="login"),
    path("logout/", views.salir, name="logout"),
    path("registro/", views.registro, name="registro"),
     # Todo lo que empiece con "facturacion/" lo atiende facturacion/urls.py
    path("facturacion/", include("facturacion.urls")),
]

# ==========================================================
# CONFIGURACIÓN PARA MOSTRAR IMÁGENES EN DESARROLLO
# ==========================================================

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

