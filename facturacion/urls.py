from django.urls import path               # path() une una dirección con una vista
from . import views                        # Las vistas de ESTA app (facturacion/views.py)

app_name = "facturacion"                   # "Apellido" de las URLs de esta app. En templates: 'facturacion:marca_lista'

urlpatterns = [
    # ---------- MARCAS: funciones (VBF) ----------
    path("marcas/", views.MarcaListView.as_view(), name="marca_lista"),

    # En los pasos siguientes agregarás aquí crear, editar y eliminar
    
    path("marcas/crear/", views.MarcaCreateView.as_view(), name="marca_crear"),
       # <int:pk> captura el número de la URL y se lo pasa a la vista como parámetro pk
    path("marcas/editar/<int:pk>/", views.MarcaUpdateView.as_view(), name="marca_editar"),
    path("marcas/eliminar/<int:pk>/", views.MarcaDeleteView.as_view(), name="marca_eliminar"),
         # TAREA 2 - CATEGORÍAS
    path("categorias/", views.CategoriaListView.as_view(), name="categoria_lista"),
    path("categorias/crear/", views.CategoriaCreateView.as_view(), name="categoria_crear"), 
    path("categorias/editar/<int:pk>/", views.CategoriaUpdateView.as_view(), name="categoria_editar"), 
    path("categorias/eliminar/<int:pk>/", views.CategoriaDeleteView.as_view(), name="categoria_eliminar"),
    
    # TAREA 3 - CLIENTES
    # ==========================
    path("clientes/", views.ClienteListView.as_view(), name="cliente_lista"),
    path("clientes/crear/", views.ClienteCreateView.as_view(), name="cliente_crear"),
    path("clientes/editar/<int:pk>/", views.ClienteUpdateView.as_view(), name="cliente_editar"),
    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detalle"),
    path("clientes/eliminar/<int:pk>/", views.ClienteDeleteView.as_view(), name="cliente_eliminar"),
    path("proveedores/eliminar/<int:pk>/", views.ProveedorDeleteView.as_view(), name="proveedor_eliminar"),

# TAREA 4 - PROVEEDORES
# ==========================================================
    path("proveedores/", views.ProveedorListView.as_view(), name="proveedor_lista"),
    path("proveedores/crear/", views.ProveedorCreateView.as_view(), name="proveedor_crear"),
    path("proveedores/editar/<int:pk>/", views.ProveedorUpdateView.as_view(), name="proveedor_editar"),
    path("proveedores/eliminar/<int:pk>/", views.ProveedorDeleteView.as_view(), name="proveedor_eliminar"),
    
# TAREA 5 - COMPRAS CON DETALLE
# ==========================================================
    path("compras/", views.CompraListView.as_view(), name="compra_lista"),
    path("compras/crear/", views.CompraCreateView.as_view(), name="compra_crear"),
    path("compras/<int:pk>/", views.CompraDetailView.as_view(), name="compra_detalle"),
    path("compras/editar/<int:pk>/", views.CompraUpdateView.as_view(), name="compra_editar"),
    path("compras/eliminar/<int:pk>/", views.CompraDeleteView.as_view(), name="compra_eliminar"),


    # ---------- PRODUCTOS: clases (VBC) ----------
    path("productos/", views.ProductoListView.as_view(), name="producto_lista"),
    path("productos/crear/", views.ProductoCreateView.as_view(), name="producto_crear"),
    path("productos/editar/<int:pk>/", views.ProductoUpdateView.as_view(), name="producto_editar"),   # pk → get_object()
    path("productos/<int:pk>/", views.ProductoDetailView.as_view(), name="producto_detalle"),
    path("productos/eliminar/<int:pk>/", views.ProductoDeleteView.as_view(), name="producto_eliminar"),
    # ---------- VENTAS: clases (VBC) ----------
    path("ventas/", views.VentaListView.as_view(), name="venta_lista"),
    path("ventas/crear/", views.VentaCreateView.as_view(), name="venta_crear"),
    path("ventas/<int:pk>/", views.VentaDetailView.as_view(), name="venta_detalle"),
    path("ventas/editar/<int:pk>/", views.VentaUpdateView.as_view(), name="venta_editar"),
    path("ventas/eliminar/<int:pk>/", views.VentaDeleteView.as_view(), name="venta_eliminar"),
]