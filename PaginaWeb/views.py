from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, F
from django.contrib import messages
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from decimal import Decimal

from .models import (
    UnidadMedida,
    Producto,
    Movimiento,
    Alerta,
    Proveedor,
    Categoria
)




@login_required
def dashboard(request):
    total_productos = Producto.objects.filter(activo=True).count()
    total_stock = Producto.objects.aggregate(total=Sum('stock_actual'))['total'] or 0
    alertas_activas = Alerta.objects.filter(activa=True).count()

    fecha_inicio = datetime.now() - timedelta(days=30)
    productos_vendidos = (
        Movimiento.objects.filter(tipo='salida', fecha__gte=fecha_inicio)
        .values('producto__nombre')
        .annotate(total=Sum('cantidad'))
        .order_by('-total')[:5]
    )

    alertas_recientes = Alerta.objects.filter(activa=True)[:5]
    movimientos_recientes = Movimiento.objects.select_related('producto', 'usuario')[:10]

    return render(request, 'dashboard.html', {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'alertas_activas': alertas_activas,
        'productos_vendidos': productos_vendidos,
        'alertas_recientes': alertas_recientes,
        'movimientos_recientes': movimientos_recientes,
    })





@login_required
def unidades_lista(request):
    unidades = UnidadMedida.objects.all()
    return render(request, "unidades/lista.html", {"unidades": unidades})


@login_required
def unidad_crear(request):
    if request.method == "POST":
        UnidadMedida.objects.create(
            nombre=request.POST.get("nombre"),
            descripcion=request.POST.get("descripcion"),
        )
        messages.success(request, "Unidad de medida creada correctamente.")
        return redirect("unidades_lista")

    return render(request, "unidades/form.html", {"titulo": "Nueva Unidad"})


@login_required
def unidad_editar(request, id):
    unidad = get_object_or_404(UnidadMedida, id=id)

    if request.method == "POST":
        unidad.nombre = request.POST.get("nombre")
        unidad.descripcion = request.POST.get("descripcion")
        unidad.save()
        messages.success(request, "Unidad actualizada correctamente.")
        return redirect("unidades_lista")

    return render(request, "unidades/form.html", {
        "titulo": "Editar Unidad",
        "unidad": unidad
    })


@login_required
def unidad_eliminar(request, id):
    unidad = get_object_or_404(UnidadMedida, id=id)
    unidad.delete()
    messages.success(request, "Unidad eliminada.")
    return redirect("unidades_lista")





@login_required
def productos_lista(request):
    productos = Producto.objects.select_related("unidad_base").all()
    return render(request, "productos/lista.html", {"productos": productos})


@login_required
def producto_crear(request):
    unidades = UnidadMedida.objects.all()

    if request.method == "POST":
        Producto.objects.create(
            codigo=request.POST.get("codigo"),
            nombre=request.POST.get("nombre"),
            unidad_base_id=request.POST.get("unidad_base"),
            stock_minimo=request.POST.get("stock_minimo"),
            descripcion=request.POST.get("descripcion"),
        )
        messages.success(request, "Producto creado correctamente.")
        return redirect("productos_lista")

    return render(request, "productos/form.html", {
        "titulo": "Nuevo Producto",
        "unidades": unidades,
        "producto": None
    })


@login_required
def producto_editar(request, id):
    producto = get_object_or_404(Producto, id=id)
    unidades = UnidadMedida.objects.all()

    if request.method == "POST":
        producto.codigo = request.POST.get("codigo")
        producto.nombre = request.POST.get("nombre")
        producto.unidad_base_id = request.POST.get("unidad_base")
        producto.stock_minimo = request.POST.get("stock_minimo")
        producto.descripcion = request.POST.get("descripcion")
        producto.save()

        messages.success(request, "Producto actualizado correctamente.")
        return redirect("productos_lista")

    return render(request, "productos/form.html", {
        "titulo": "Editar Producto",
        "producto": producto,
        "unidades": unidades
    })
@login_required
def proveedor_crear(request):
    if request.method == "POST":
        Proveedor.objects.create(
            nombre=request.POST.get("nombre"),
            telefono=request.POST.get("telefono"),
            email=request.POST.get("email"),
            direccion=request.POST.get("direccion"),
        )
        messages.success(request, "Proveedor registrado correctamente.")
        return redirect("movimiento_crear")  
    return render(request, "proveedores/form.html")


@login_required
def producto_eliminar(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Producto eliminado correctamente.")
    return redirect("productos_lista")





@login_required
def movimientos_lista(request):
    movimientos = Movimiento.objects.select_related("producto", "usuario").all()
    return render(request, "movimientos/lista.html", {"movimientos": movimientos})


@login_required
def movimiento_crear(request):
    from decimal import Decimal

    productos = Producto.objects.all()
    proveedores = Proveedor.objects.filter(activo=True)

    if request.method == "POST":

        producto_id = request.POST.get("producto")
        tipo = request.POST.get("tipo")
        proveedor_id = request.POST.get("proveedor") or None
        motivo = request.POST.get("motivo")

        
        if not producto_id:
            messages.error(request, "Debe seleccionar un producto.")
            return redirect("movimiento_crear")

        if tipo == "entrada" and not proveedor_id:
            messages.error(request, "Debe seleccionar un proveedor para movimientos de entrada.")
            return redirect("movimiento_crear")

        cantidad = request.POST.get("cantidad")

        try:
            cantidad = Decimal(cantidad)
        except:
            messages.error(request, "Cantidad inválida.")
            return redirect("movimiento_crear")

        producto_obj = Producto.objects.get(id=producto_id)

        movimiento = Movimiento.objects.create(
            producto=producto_obj,
            tipo=tipo,
            unidad_ingreso=producto_obj.unidad_base,
            cantidad=cantidad,
            factor=Decimal(1),
            proveedor_id=proveedor_id,
            motivo=motivo,
            usuario=request.user
        )

        messages.success(request, "Movimiento registrado correctamente.")
        return redirect("movimientos_lista")

    return render(request, "movimientos/form.html", {
        "productos": productos,
        "proveedores": proveedores
    })


@login_required
def inventario(request):
    categoria_id = request.GET.get('categoria')
    estado = request.GET.get('estado')
    busqueda = request.GET.get('busqueda')

    productos = Producto.objects.filter(activo=True)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if estado == 'critico':
        productos = productos.filter(stock_actual__lt=F('stock_minimo'))
    elif estado == 'bajo':
        productos = productos.filter(
            stock_actual__gte=F('stock_minimo'),
            stock_actual__lt=F('stock_minimo') * 1.5
        )

    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | Q(codigo__icontains=busqueda)
        )

    return render(request, 'inventario.html', {
        'productos': productos,
        'categorias': Categoria.objects.all()
    })


@login_required
def proveedores(request):
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'proveedores.html', {"proveedores": proveedores})


@login_required
def reportes(request):
    return render(request, 'reportes.html')


@login_required
def alertas(request):
    alertas = Alerta.objects.filter(activa=True).select_related('producto')
    return render(request, 'alertas.html', {"alertas": alertas})
