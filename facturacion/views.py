from django.contrib import messages                          # mensajes verdes / rojos
from django.contrib.auth.mixins import LoginRequiredMixin   # exige sesión (el @login_required de las clases)
from django.contrib.messages.views import SuccessMessageMixin   # mensaje de éxito automático
from django.db import transaction                            # transaction.atomic(): todo o nada
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from .forms import MarcaForm, CategoriaForm, ClienteForm, ProveedorForm, ProductoForm, VentaForm, DetalleVentaFormSet, CompraForm, DetalleCompraFormSet
from .mixins import UsuarioRegistroMixin
from .models import Categoria, Cliente, Marca, Producto, Proveedor, Venta, TipoPago, IVA_TARIFA, Compra  # Modelos del sistema


# ==========================================================
# TAREA 1 - MARCAS: LISTAR CON VISTAS BASADAS EN CLASES
# ==========================================================

class MarcaListView(LoginRequiredMixin, ListView):
    # Modelo del que consultamos los registros.
    model = Marca

    # Archivo HTML que mostrará la lista de marcas.
    template_name = "facturacion/marca_lista.html"

    # Nombre que utilizamos para recorrer las marcas en HTML.
    context_object_name = "marcas"

    # Mostramos un máximo de cinco registros por página.
    paginate_by = 5

    # Título que enviamos a la plantilla.
    extra_context = {"titulo": "Marcas"}

    def get_queryset(self):
        # Obtenemos las marcas registradas.
        registros = super().get_queryset()

        # Recuperamos el texto escrito en el buscador.
        q = self.request.GET.get("q", "").strip()

        # Filtramos las marcas cuando se realiza una búsqueda.
        if q:
            registros = registros.filter(nombre__icontains=q)

        return registros

    def get_context_data(self, **kwargs):
        # Recuperamos el contexto que prepara Django.
        contexto = super().get_context_data(**kwargs)

        # Conservamos el texto del buscador en el formulario.
        contexto["q"] = self.request.GET.get("q", "")

        return contexto



# ==========================================================
# TAREA 1 - MARCAS: CREAR CON VISTAS BASADAS EN CLASES
# ==========================================================

class MarcaCreateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, CreateView):
    # Seleccionamos el modelo para registrar las marcas.
    model = Marca

    # Utilizamos el formulario que ya existe en forms.py.
    form_class = MarcaForm

    # Indicamos el HTML que mostrará los campos.
    template_name = "facturacion/marca_form.html"

    # Al guardar, regresamos al listado de marcas.
    success_url = reverse_lazy("facturacion:marca_lista")

    # Mostramos un mensaje cuando se registra la marca.
    success_message = "Marca «%(nombre)s» creada correctamente."

    # Enviamos el título y el texto del botón al HTML.
    extra_context = {
        "titulo": "Nueva marca",
        "boton": "Guardar"
    }


# ==========================================================
# TAREA 1 - MARCAS: EDITAR CON VISTAS BASADAS EN CLASES
# ==========================================================

class MarcaUpdateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, UpdateView):
    # Modelo en el que actualizaremos los datos.
    model = Marca

    # Reutilizamos el formulario de marcas.
    form_class = MarcaForm

    # Utilizamos el mismo HTML de crear marcas.
    template_name = "facturacion/marca_form.html"

    # Después de editar, regresamos al listado.
    success_url = reverse_lazy("facturacion:marca_lista")

    # Mensaje que aparece al actualizar correctamente.
    success_message = "Marca «%(nombre)s» actualizada correctamente."

    # Configuramos el título y el botón del formulario.
    extra_context = {
        "titulo": "Editar marca",
        "boton": "Actualizar"
    }

    def form_invalid(self, form):
        # Avisamos al usuario cuando existen errores en los datos.
        messages.error(self.request, "Revisa los campos del formulario.")

        # Regresamos al formulario para mostrar los errores.
        return super().form_invalid(form)





# ==========================================================
# TAREA 1 - MARCAS: ELIMINAR CON VISTAS BASADAS EN CLASES
# ==========================================================

class MarcaDeleteView(LoginRequiredMixin, DeleteView):
    # Modelo del que eliminaremos un registro.
    model = Marca

    # Página donde el usuario confirma la eliminación.
    template_name = "facturacion/marca_eliminar.html"

    # Nombre que utilizaremos para mostrar la marca en HTML.
    context_object_name = "marca"

    # Página a la que regresamos después de eliminar.
    success_url = reverse_lazy("facturacion:marca_lista")

    # Título de la página.
    extra_context = {"titulo": "Eliminar marca"}

    def form_valid(self, form):
        # Guardamos el nombre antes de intentar eliminar.
        nombre = self.object.nombre

        try:
            # Django intenta eliminar la marca seleccionada.
            respuesta = super().form_valid(form)

        except ProtectedError:
            # Si tiene productos asociados, impedimos eliminarla.
            messages.error(
                self.request,
                f"No se puede eliminar «{nombre}» porque tiene productos asociados. Desactívala en su lugar."
            )

            # Regresamos al listado sin eliminar la marca.
            return redirect("facturacion:marca_lista")

        # Mostramos el mensaje si la eliminación fue exitosa.
        messages.success(
            self.request,
            f"Marca «{nombre}» eliminada correctamente."
        )

        return respuesta
# ==========================================================
# TAREA 2 - CATEGORÍAS: LISTADO CON VBC
# ==========================================================

class CategoriaListView(LoginRequiredMixin, ListView):
    # Modelo del que vamos a obtener las categorías.
    model = Categoria

    # Plantilla HTML que mostrará los registros.
    template_name = "facturacion/categoria_lista.html"

    # Nombre con el que recorreremos los registros en HTML.
    context_object_name = "categorias"

    # Mostramos cinco categorías por página.
    paginate_by = 5

    # Título que enviamos a la plantilla.
    extra_context = {"titulo": "Categorías"}

    def get_queryset(self):
        # Consultamos las categorías registradas.
        categorias = super().get_queryset()

        # Leemos lo que escribió el usuario en el buscador.
        q = self.request.GET.get("q", "").strip()

        # Si escribió algo, buscamos por el nombre.
        if q:
            categorias = categorias.filter(nombre__icontains=q)

        return categorias

    def get_context_data(self, **kwargs):
        # Recuperamos el contexto generado por Django.
        contexto = super().get_context_data(**kwargs)

        # Conservamos el texto de la búsqueda.
        contexto["q"] = self.request.GET.get("q", "")

        return contexto
    

# ==========================================================
# TAREA 2 - CATEGORÍAS: CREAR CON VBC
# ==========================================================

class CategoriaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    # Modelo donde guardaremos la nueva categoría.
    model = Categoria

    # Formulario que creamos en forms.py.
    form_class = CategoriaForm

    # Plantilla que mostrará el formulario.
    template_name = "facturacion/categoria_form.html"

    # Regresamos al listado después de guardar.
    success_url = reverse_lazy("facturacion:categoria_lista")

    # Mensaje que aparecerá al registrar una categoría.
    success_message = "Categoría «%(nombre)s» creada correctamente."

    # Título y nombre del botón.
    extra_context = {
        "titulo": "Nueva categoría",
        "boton": "Guardar"
    }

# ==========================================================
# TAREA 2 - CATEGORÍAS: EDITAR CON VBC
# ==========================================================

class CategoriaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    # Modelo que contiene las categorías.
    model = Categoria

    # Reutilizamos el formulario existente.
    form_class = CategoriaForm

    # Utilizamos el mismo HTML para crear y editar.
    template_name = "facturacion/categoria_form.html"

    # Al actualizar, regresamos al listado.
    success_url = reverse_lazy("facturacion:categoria_lista")

    # Mensaje de confirmación.
    success_message = "Categoría «%(nombre)s» actualizada correctamente."

    # Configuramos el título y el botón.
    extra_context = {
        "titulo": "Editar categoría",
        "boton": "Actualizar"
    }


# ==========================================================
# TAREA 2 - CATEGORÍAS: ELIMINAR CON VBC
# ==========================================================

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    # Modelo que contiene las categorías.
    model = Categoria

    # HTML donde confirmaremos la eliminación.
    template_name = "facturacion/categoria_eliminar.html"

    # Nombre que utilizaremos en el HTML.
    context_object_name = "categoria"

    # Después de eliminar, volvemos al listado.
    success_url = reverse_lazy("facturacion:categoria_lista")

    # Título de la página.
    extra_context = {"titulo": "Eliminar categoría"}

    def form_valid(self, form):
        # Guardamos el nombre antes de eliminar.
        nombre = self.object.nombre

        # Ejecutamos la eliminación mediante DeleteView.
        respuesta = super().form_valid(form)

        # Mostramos un mensaje de confirmación.
        messages.success(
            self.request,
            f"Categoría «{nombre}» eliminada correctamente."
        )

        return respuesta

# ==========================================================
# TAREA 3 - CLIENTES: LISTADO CON VBC
# ==========================================================

class ClienteListView(LoginRequiredMixin, ListView):
    # Modelo que contiene los clientes registrados.
    model = Cliente

    # Archivo HTML donde mostraremos los clientes.
    template_name = "facturacion/cliente_lista.html"

    # Nombre que utilizaremos en la plantilla.
    context_object_name = "clientes"

    # Mostramos cinco clientes por página.
    paginate_by = 5

    # Título del listado.
    extra_context = {"titulo": "Clientes"}

    def get_queryset(self):
        # Obtenemos los clientes registrados.
        clientes = super().get_queryset()

        # Recuperamos el texto ingresado en el buscador.
        q = self.request.GET.get("q", "").strip()

        # Buscamos por apellido O por cédula.
        if q:
            clientes = clientes.filter(
                Q(apellidos__icontains=q) |
                Q(cedula__icontains=q)
            )

        return clientes

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto generado por Django.
        contexto = super().get_context_data(**kwargs)

        # Conservamos el texto que escribió el usuario.
        contexto["q"] = self.request.GET.get("q", "")

        return contexto


# ==========================================================
# TAREA 3 - CLIENTES: CREAR CON VISTAS BASADAS EN CLASES
# ==========================================================

class ClienteCreateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, CreateView):
    # Modelo donde guardaremos los clientes.
    model = Cliente

    # Formulario con validación de cédula.
    form_class = ClienteForm

    # Archivo HTML que mostrará los campos.
    template_name = "facturacion/cliente_form.html"

    # Después de guardar, regresamos al listado.
    success_url = reverse_lazy("facturacion:cliente_lista")

    # Mensaje cuando se registra un cliente.
    success_message = "Cliente registrado correctamente."

    # Personalizamos el título y el botón.
    extra_context = {
        "titulo": "Nuevo cliente",
        "boton": "Guardar"
    }
    

# ==========================================================
# TAREA 3 - CLIENTES: EDITAR CON VBC
# ==========================================================

class ClienteUpdateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, UpdateView):
    # Modelo que contiene los clientes registrados.
    model = Cliente

    # Reutilizamos el formulario con validación de cédula.
    form_class = ClienteForm

    # El mismo HTML sirve para crear y editar clientes.
    template_name = "facturacion/cliente_form.html"

    # Después de actualizar, regresamos al listado.
    success_url = reverse_lazy("facturacion:cliente_lista")

    # Mensaje que se mostrará al actualizar.
    success_message = "Cliente actualizado correctamente."

    # Configuramos el título y el botón del formulario.
    extra_context = {
        "titulo": "Editar cliente",
        "boton": "Actualizar"
    }


# ==========================================================
# TAREA 3 - CLIENTES: DETALLE E HISTORIAL DE VENTAS
# ==========================================================

class ClienteDetailView(LoginRequiredMixin, DetailView):
    # Modelo que contiene los datos del cliente.
    model = Cliente

    # HTML donde mostraremos su información.
    template_name = "facturacion/cliente_detalle.html"

    # Nombre que utilizaremos en la plantilla.
    context_object_name = "cliente"

    # Título de la pantalla.
    extra_context = {
        "titulo": "Detalle del cliente"
    }


# ==========================================================
# TAREA 3 - CLIENTES: ELIMINAR CON VBC
# ==========================================================

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    # Modelo que contiene los clientes registrados.
    model = Cliente

    # Pantalla para confirmar la eliminación.
    template_name = "facturacion/cliente_eliminar.html"

    # Nombre que utilizaremos en el archivo HTML.
    context_object_name = "cliente"

    # Después de eliminar, regresamos al listado.
    success_url = reverse_lazy("facturacion:cliente_lista")

    # Título de la pantalla.
    extra_context = {
        "titulo": "Eliminar cliente"
    }

    def form_valid(self, form):
        # Guardamos el nombre antes de intentar eliminar.
        nombre = f"{self.object.nombres} {self.object.apellidos}"

        try:
            # Intentamos eliminar el cliente.
            respuesta = super().form_valid(form)

        except ProtectedError:
            # Si tiene ventas asociadas, no permitimos eliminarlo.
            messages.error(
                self.request,
                f"No se puede eliminar a {nombre} porque tiene ventas registradas."
            )

            return redirect("facturacion:cliente_lista")

        # Confirmamos la eliminación exitosa.
        messages.success(
            self.request,
            f"Cliente {nombre} eliminado correctamente."
        )

        return respuesta


# ==========================================================
# TAREA 4 - PROVEEDORES: LISTADO CON VBC
# ==========================================================

class ProveedorListView(LoginRequiredMixin, ListView):
    # Modelo del que consultaremos los proveedores.
    model = Proveedor

    # HTML donde mostraremos los proveedores.
    template_name = "facturacion/proveedor_lista.html"

    # Nombre utilizado para recorrer los registros en HTML.
    context_object_name = "proveedores"

    # Mostramos cinco proveedores por página.
    paginate_by = 5

    # Título enviado a la plantilla.
    extra_context = {"titulo": "Proveedores"}

    def get_queryset(self):
        # Recuperamos los proveedores registrados.
        proveedores = super().get_queryset()

        # Obtenemos el texto escrito en el buscador.
        q = self.request.GET.get("q", "").strip()

        # Buscamos por nombre, apellido o RUC.
        if q:
            proveedores = proveedores.filter(
                Q(nombre__icontains=q) |
                Q(apellido__icontains=q) |
                Q(ruc__icontains=q)
            )

        return proveedores

    def get_context_data(self, **kwargs):
        # Recuperamos el contexto preparado por Django.
        contexto = super().get_context_data(**kwargs)

        # Conservamos el texto ingresado en el buscador.
        contexto["q"] = self.request.GET.get("q", "")

        return contexto

# ==========================================================
# TAREA 4 - PROVEEDORES: CREAR CON VBC
# ==========================================================

class ProveedorCreateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, CreateView):
    # Modelo donde registraremos los proveedores.
    model = Proveedor

    # Formulario que valida el RUC y permite subir el logo.
    form_class = ProveedorForm

    # Archivo HTML que mostrará los campos del proveedor.
    template_name = "facturacion/proveedor_form.html"

    # Después de guardar, regresamos al listado.
    success_url = reverse_lazy("facturacion:proveedor_lista")

    # Mensaje que aparecerá al registrar correctamente.
    success_message = "Proveedor registrado correctamente."

    # Personalizamos el título y el botón del formulario.
    extra_context = {
        "titulo": "Nuevo proveedor",
        "boton": "Guardar"
    }

# ==========================================================
# TAREA 4 - PROVEEDORES: EDITAR CON VBC
# ==========================================================

class ProveedorUpdateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, UpdateView):
    # Modelo que contiene los proveedores registrados.
    model = Proveedor

    # Reutilizamos el formulario que valida el RUC.
    form_class = ProveedorForm

    # El mismo HTML sirve para crear y editar.
    template_name = "facturacion/proveedor_form.html"

    # Regresamos al listado después de actualizar.
    success_url = reverse_lazy("facturacion:proveedor_lista")

    # Mensaje de confirmación.
    success_message = "Proveedor actualizado correctamente."

    # Personalizamos el título y el botón.
    extra_context = {
        "titulo": "Editar proveedor",
        "boton": "Actualizar"
    }

# ==========================================================
# TAREA 4 - PROVEEDORES: ELIMINAR CON VBC
# ==========================================================

class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    # Modelo que contiene los proveedores registrados.
    model = Proveedor

    # Plantilla para confirmar la eliminación.
    template_name = "facturacion/proveedor_eliminar.html"

    # Nombre utilizado en el archivo HTML.
    context_object_name = "proveedor"

    # Después de eliminar, regresamos al listado.
    success_url = reverse_lazy("facturacion:proveedor_lista")

    # Título que mostramos en la pantalla.
    extra_context = {
        "titulo": "Eliminar proveedor"
    }

    def form_valid(self, form):
        # Guardamos el nombre antes de eliminar el registro.
        nombre = f"{self.object.nombre} {self.object.apellido}"

        try:
            # Intentamos eliminar el proveedor.
            respuesta = super().form_valid(form)

        except ProtectedError:
            # Protegemos a los proveedores con compras asociadas.
            messages.error(
                self.request,
                f"No se puede eliminar a {nombre} porque tiene compras registradas."
            )

            return redirect("facturacion:proveedor_lista")

        # Confirmamos que el registro fue eliminado.
        messages.success(
            self.request,
            f"Proveedor {nombre} eliminado correctamente."
        )

        return respuesta


class ProductoListView(LoginRequiredMixin, ListView):     # LISTAR
    model = Producto                                       # ¿qué tabla?
    template_name = "facturacion/producto_lista.html"      # ¿qué HTML?
    context_object_name = "productos"                      # nombre de la lista en el HTML
    paginate_by = 5                                        # 5 por página → envía page_obj
    extra_context = {"titulo": "Productos"} 
    
    def get_queryset(self):                                # ¿QUÉ registros se muestran?
        productos = super().get_queryset()                 # lo normal: Producto.objects.all()
        productos = productos.select_related("marca").prefetch_related("categorias")   # menos consultas
        q = self.request.GET.get("q", "")                  # buscador: ?q=galaxy
        if q:
            productos = productos.filter(nombre__icontains=q)
        return productos

    def get_context_data(self, **kwargs):                  # ¿qué datos EXTRA recibe el HTML?
        contexto = super().get_context_data(**kwargs) 
        # lo que ListView ya armó
        contexto["q"] = self.request.GET.get("q", "")      # + lo buscado
        return contexto


class ProductoCreateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, CreateView):   # CREAR
    model = Producto
    form_class = ProductoForm                              # nuestro formulario
    template_name = "facturacion/producto_form.html"
    success_url = reverse_lazy("facturacion:producto_lista")   # a dónde ir al guardar
    success_message = "Producto «%(nombre)s» creado."      # %(nombre)s = el campo nombre del formulario
    extra_context = {"titulo": "Nuevo producto", "boton": "Guardar"}

   
class ProductoUpdateView(LoginRequiredMixin, UsuarioRegistroMixin, SuccessMessageMixin, UpdateView):   # EDITAR
    model = Producto
    form_class = ProductoForm
    template_name = "facturacion/producto_form.html"       # el mismo template de crear
    success_url = reverse_lazy("facturacion:producto_lista")
    success_message = "Producto «%(nombre)s» actualizado."
    extra_context = {"titulo": "Editar producto", "boton": "Actualizar"}

    def form_invalid(self, form):                          # cuando hay errores (POST inválido)
        messages.error(self.request, "Revisa los campos marcados en rojo.")
        return super().form_invalid(form)                  # vuelve a mostrar el formulario

class ProductoDetailView(LoginRequiredMixin, DetailView):  # VER UNO
    model = Producto
    template_name = "facturacion/producto_detalle.html"
    context_object_name = "producto"

class ProductoDeleteView(LoginRequiredMixin, DeleteView):  # ELIMINAR
    model = Producto
    template_name = "facturacion/producto_eliminar.html"
    context_object_name = "producto"
    success_url = reverse_lazy("facturacion:producto_lista")

    def form_valid(self, form):                            # se ejecuta al confirmar (POST)
        nombre = self.object.nombre                        # self.object = el producto a eliminar
        try:
            respuesta = super().form_valid(form)           # DELETE + redirect
        except ProtectedError:                             # ya está en una venta o compra (PROTECT)
            messages.error(self.request, f"No se puede eliminar «{nombre}»: ya tiene ventas o compras. Desactívalo.")
            return redirect("facturacion:producto_lista")
        messages.success(self.request, f"Producto «{nombre}» eliminado.")
        return respuesta

# ================= Ventas ===================
class VentaDetallesMixin:
    """Lo que COMPARTEN crear y editar una venta: cabecera (form) + filas (formset)."""
    model = Venta
    form_class = VentaForm
    template_name = "facturacion/venta_form.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)      # trae "form" (la cabecera)
        if "detalles" not in contexto:                     # en GET el formset todavía no existe...
            contexto["detalles"] = DetalleVentaFormSet(instance=self.object)   # ...lo creamos (vacío o lleno)
        return contexto

    def post(self, request, *args, **kwargs):              # REEMPLAZA el post() normal de la vista
        form = self.get_form()                             # 1. cabecera con request.POST
        detalles = DetalleVentaFormSet(request.POST, instance=self.object)   # 2. filas con request.POST
        if form.is_valid() and detalles.is_valid():        # 3. ¿las DOS partes están bien?
            return self.form_valid(form, detalles)
        return self.form_invalid(form, detalles)

    def form_valid(self, form, detalles):
        with transaction.atomic(): 
           # TODO o NADA: si algo falla, se deshace todo
            if self.object:                                # al EDITAR: devolver lo que la venta tenía
                self.object.devolver_stock()
            form.instance.user = self.request.user
            self.object = form.save()                      # INSERT o UPDATE de la cabecera
            self.guardar_detalles(detalles)                # INSERT / UPDATE / DELETE de las filas
            self.object.descontar_stock()                  # saca de bodega lo vendido
            self.object.calcular_totales()                 # subtotal, IVA y total
        messages.success(self.request, f"{self.object} guardada. Total: ${self.object.total}")
        return HttpResponseRedirect(self.get_success_url())

    def guardar_detalles(self, detalles):
        detalles.instance = self.object                    # las filas pertenecen a ESTA venta
        filas = detalles.save(commit=False)                # objetos nuevos o cambiados, SIN guardar todavía
        for fila in detalles.deleted_objects:              # filas con la casilla "Quitar"
            fila.delete()
        cambio_producto = {obj.pk for obj, campos in detalles.changed_objects if "producto" in campos}
        for fila in filas:
            if fila.pk is None or fila.pk in cambio_producto:   # fila nueva o con otro producto...
                fila.precio = fila.producto.precio              # ...toma el precio ACTUAL del producto
            fila.user = self.request.user
            fila.save()

    def form_invalid(self, form, detalles):
        messages.error(self.request, "Revisa los datos de la venta.")
        # volvemos a dibujar la página con la cabecera Y las filas, con sus errores
        return self.render_to_response(self.get_context_data(form=form, detalles=detalles))

    def get_success_url(self):
        return reverse("facturacion:venta_detalle", kwargs={"pk": self.object.pk})   # a la factura
class VentaListView(LoginRequiredMixin, ListView):
    model = Venta
    template_name = "facturacion/venta_lista.html"
    context_object_name = "ventas"
    paginate_by = 10
    extra_context = {"titulo": "Ventas", "tipos_pago": TipoPago.choices}   # opciones para el filtro

    def get_queryset(self):
        ventas = super().get_queryset().select_related("cliente")   # trae el cliente en el mismo JOIN
        q = self.request.GET.get("q", "")
        tipo = self.request.GET.get("tipo_pago", "")
        if q:   # Q(...) | Q(...) = condición con OR: por apellido O por cédula
            ventas = ventas.filter(Q(cliente__apellidos__icontains=q) | Q(cliente__cedula__icontains=q))
        if tipo:
            ventas = ventas.filter(tipo_pago=tipo)
        return ventas

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["q"] = self.request.GET.get("q", "")
        contexto["tipo_pago"] = self.request.GET.get("tipo_pago", "")
        return contexto

class VentaCreateView(LoginRequiredMixin, VentaDetallesMixin, CreateView):   # CREAR
    extra_context = {"titulo": "Nueva venta", "boton": "Guardar venta"}

    def post(self, request, *args, **kwargs):
        self.object = None                                 # CreateView: aún no hay venta
        return super().post(request, *args, **kwargs)      # sigue al post() del mixin
class VentaUpdateView(LoginRequiredMixin, VentaDetallesMixin, UpdateView):   # EDITAR
    extra_context = {"titulo": "Editar venta", "boton": "Actualizar venta"}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()                    # UpdateView: la venta del <int:pk>
        return super().post(request, *args, **kwargs)
class VentaDetailView(LoginRequiredMixin, DetailView):     # VER (la factura)
    model = Venta
    template_name = "facturacion/venta_detalle.html"
    context_object_name = "venta"

    def get_queryset(self):
        return super().get_queryset().select_related("cliente", "user").prefetch_related("detalles__producto")

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["iva_porcentaje"] = IVA_TARIFA * 100      # 15
        return contexto
    
class VentaDeleteView(LoginRequiredMixin, DeleteView):     # ELIMINAR
    model = Venta
    template_name = "facturacion/venta_eliminar.html"
    context_object_name = "venta"
    success_url = reverse_lazy("facturacion:venta_lista")

    def form_valid(self, form):
        with transaction.atomic():
            self.object.devolver_stock()                   # 1. los productos regresan a la bodega
            respuesta = super().form_valid(form)           # 2. DELETE de la venta (CASCADE borra sus detalles)
        messages.success(self.request, "Venta eliminada y stock devuelto.")
        return respuesta


# ==========================================================
# TAREA 5 - COMPRAS: MANEJO DE DETALLES Y STOCK
# ==========================================================

class CompraDetallesMixin:
    # Modelo y formulario principal de compras.
    model = Compra
    form_class = CompraForm
    template_name = "facturacion/compra_form.html"

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Enviamos los detalles a la plantilla.
        if "detalles" not in contexto:
            contexto["detalles"] = DetalleCompraFormSet(
                instance=self.object
            )

        return contexto

    def post(self, request, *args, **kwargs):
        # Recibimos los datos principales.
        form = self.get_form()

        # Recibimos los productos de la compra.
        detalles = DetalleCompraFormSet(
            request.POST,
            instance=self.object
        )

        # Validamos ambas partes.
        if form.is_valid() and detalles.is_valid():
            return self.form_valid(form, detalles)

        return self.form_invalid(form, detalles)

    def form_valid(self, form, detalles):
        # Guardamos toda la operación en una transacción.
        with transaction.atomic():

            # Al editar, revertimos primero el stock anterior.
            if self.object is not None:
                self.object.revertir_stock()

            # Registramos al usuario responsable.
            form.instance.user = self.request.user

            # Guardamos la cabecera de la compra.
            self.object = form.save()

            # Relacionamos los detalles con la compra.
            detalles.instance = self.object

            # Preparamos los detalles sin guardarlos todavía.
            filas = detalles.save(commit=False)

            # Eliminamos las filas marcadas para quitar.
            for fila in detalles.deleted_objects:
                fila.delete()

            # Guardamos cada producto y su costo.
            for fila in filas:
                fila.compra = self.object
                fila.user = self.request.user
                fila.save()

            # Aumentamos las existencias.
            self.object.ingresar_stock()

            # Calculamos subtotal, IVA y total.
            self.object.calcular_totales()

        messages.success(
            self.request,
            "Compra guardada correctamente."
        )

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, detalles):
        messages.error(
            self.request,
            "Revisa los datos ingresados en la compra."
        )

        return self.render_to_response(
            self.get_context_data(
                form=form,
                detalles=detalles
            )
        )

    def get_success_url(self):
        # Al guardar, mostraremos el detalle de la compra.
        return reverse(
            "facturacion:compra_detalle",
            kwargs={"pk": self.object.pk}
        )



# ==========================================================
# TAREA 5 - COMPRAS: LISTADO CON VBC
# ==========================================================

class CompraListView(LoginRequiredMixin, ListView):
    # Modelo de las compras.
    model = Compra

    # Plantilla donde mostraremos el listado.
    template_name = "facturacion/compra_lista.html"

    # Nombre utilizado para recorrer las compras.
    context_object_name = "compras"

    # Mostramos diez compras por página.
    paginate_by = 10

    # Título y opciones del filtro.
    extra_context = {
        "titulo": "Compras",
        "tipos_pago": TipoPago.choices
    }

    def get_queryset(self):
        # Consultamos las compras con sus proveedores.
        compras = super().get_queryset().select_related(
            "proveedor"
        )

        # Recuperamos los filtros del buscador.
        q = self.request.GET.get("q", "").strip()
        tipo = self.request.GET.get("tipo_pago", "")

        # Buscamos por nombre, apellido o RUC.
        if q:
            compras = compras.filter(
                Q(proveedor__nombre__icontains=q) |
                Q(proveedor__apellido__icontains=q) |
                Q(proveedor__ruc__icontains=q)
            )

        # Filtramos por el tipo de pago.
        if tipo:
            compras = compras.filter(tipo_pago=tipo)

        return compras

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)

        # Conservamos los filtros seleccionados.
        contexto["q"] = self.request.GET.get("q", "")
        contexto["tipo_pago"] = self.request.GET.get(
            "tipo_pago", ""
        )

        return contexto



# ==========================================================
# TAREA 5 - COMPRAS: CREAR CON VBC
# ==========================================================

class CompraCreateView(LoginRequiredMixin, CompraDetallesMixin, CreateView):

    # Personalizamos el título y el botón.
    extra_context = {
        "titulo": "Nueva compra",
        "boton": "Guardar compra"
    }

    def post(self, request, *args, **kwargs):
        # Como es una compra nueva, todavía no existe.
        self.object = None

        # Continuamos con el proceso del mixin.
        return super().post(request, *args, **kwargs)



# ==========================================================
# TAREA 5 - COMPRAS: CONSULTAR DETALLE CON VBC
# ==========================================================

class CompraDetailView(LoginRequiredMixin, DetailView):
    # Modelo que contiene las compras registradas.
    model = Compra

    # Archivo HTML donde mostraremos el detalle.
    template_name = "facturacion/compra_detalle.html"

    # Nombre que utilizaremos en el HTML.
    context_object_name = "compra"

    def get_queryset(self):
        # Consultamos la compra con su proveedor y productos.
        return super().get_queryset().select_related(
            "proveedor", "user"
        ).prefetch_related(
            "detalles__producto"
        )

    def get_context_data(self, **kwargs):
        # Recuperamos la información de la compra.
        contexto = super().get_context_data(**kwargs)

        # Porcentaje de IVA utilizado en el sistema.
        contexto["iva_porcentaje"] = IVA_TARIFA * 100

        return contexto



# ==========================================================
# TAREA 5 - COMPRAS: EDITAR CON VBC
# ==========================================================

class CompraUpdateView(LoginRequiredMixin, CompraDetallesMixin, UpdateView):

    # Datos que aparecerán al editar una compra.
    extra_context = {
        "titulo": "Editar compra",
        "boton": "Actualizar compra"
    }

    def post(self, request, *args, **kwargs):
        # Recuperamos la compra que vamos a modificar.
        self.object = self.get_object()

        # Continuamos con el proceso del mixin.
        return super().post(request, *args, **kwargs)



# ==========================================================
# TAREA 5 - COMPRAS: ELIMINAR CON VBC
# ==========================================================

class CompraDeleteView(LoginRequiredMixin, DeleteView):
    # Modelo que contiene las compras.
    model = Compra

    # Pantalla para confirmar la eliminación.
    template_name = "facturacion/compra_eliminar.html"

    # Nombre utilizado dentro del HTML.
    context_object_name = "compra"

    # Después de eliminar, regresamos al listado.
    success_url = reverse_lazy("facturacion:compra_lista")

    def form_valid(self, form):

        # La eliminación y el ajuste de stock se hacen juntos.
        with transaction.atomic():

            # Sumamos las cantidades por producto.
            cantidades = {}

            for detalle in self.object.detalles.all():
                producto_id = detalle.producto_id

                cantidades[producto_id] = (
                    cantidades.get(producto_id, 0)
                    + detalle.cantidad
                )

            # Comprobamos que el stock sea suficiente.
            productos = Producto.objects.select_for_update().filter(
                pk__in=cantidades
            )

            for producto in productos:
                if producto.stock < cantidades[producto.pk]:
                    messages.error(
                        self.request,
                        f"No se puede eliminar la compra: "
                        f"stock insuficiente de {producto.nombre}."
                    )

                    return redirect("facturacion:compra_lista")

            # Revertimos las unidades de la compra.
            self.object.revertir_stock()

            # Eliminamos la compra y sus detalles.
            respuesta = super().form_valid(form)

        # Mostramos el mensaje de confirmación.
        messages.success(
            self.request,
            "Compra eliminada y stock actualizado correctamente."
        )

        return respuesta
