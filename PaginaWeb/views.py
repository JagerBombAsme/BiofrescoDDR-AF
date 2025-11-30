from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from .models import Producto, Movimiento, Alerta, Proveedor, Categoria
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    # Estadísticas generales
    total_productos = Producto.objects.filter(activo=True).count()
    total_stock = Producto.objects.aggregate(total=Sum('stock_actual'))['total'] or 0
    alertas_activas = Alerta.objects.filter(activa=True).count()
    
    # Productos más vendidos (últimos 30 días)
    fecha_inicio = datetime.now() - timedelta(days=30)
    productos_vendidos = Movimiento.objects.filter(
        tipo='salida',
        fecha__gte=fecha_inicio
    ).values('producto__nombre').annotate(
        total=Sum('cantidad')
    ).order_by('-total')[:5]
    
    # Alertas recientes
    alertas_recientes = Alerta.objects.filter(activa=True)[:5]
    
    # Movimientos recientes
    movimientos_recientes = Movimiento.objects.select_related('producto', 'usuario')[:10]
    
    context = {
        'total_productos': total_productos,
        'total_stock': total_stock,
        'alertas_activas': alertas_activas,
        'productos_vendidos': productos_vendidos,
        'alertas_recientes': alertas_recientes,
        'movimientos_recientes': movimientos_recientes,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def inventario(request):
    # Filtros
    categoria_id = request.GET.get('categoria')
    estado = request.GET.get('estado')
    busqueda = request.GET.get('busqueda')
    
    productos = Producto.objects.filter(activo=True).select_related('categoria', 'proveedor')
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if estado == 'critico':
        productos = productos.filter(stock_actual__lt=models.F('stock_minimo'))
    elif estado == 'bajo':
        productos = productos.filter(
            stock_actual__gte=models.F('stock_minimo'),
            stock_actual__lt=models.F('stock_minimo') * 1.5
        )
    
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | Q(codigo__icontains=busqueda)
        )
    
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    
    return render(request, 'inventario.html', context)

@login_required
def productos(request):
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
        'categorias': categorias,
    }
    
    return render(request, 'productos.html', context)

@login_required
def producto_crear(request):
    if request.method == 'POST':
        # Aquí procesarías el formulario
        # Por ahora solo redirige
        return redirect('PaginaWeb:productos')
    
    categorias = Categoria.objects.all()
    proveedores = Proveedor.objects.filter(activo=True)
    
    context = {
        'categorias': categorias,
        'proveedores': proveedores,
    }
    
    return render(request, 'producto_form.html', context)

@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    # Lógica de edición aquí
    return redirect('PaginaWeb:productos')

@login_required
def movimientos(request):
    movimientos = Movimiento.objects.select_related('producto', 'usuario')[:50]
    
    context = {
        'movimientos': movimientos,
    }
    
    return render(request, 'movimientos.html', context)

@login_required
def movimiento_crear(request):
    # Lógica para crear movimiento
    return redirect('PaginaWeb:movimientos')

@login_required
def proveedores(request):
    proveedores = Proveedor.objects.filter(activo=True)
    
    context = {
        'proveedores': proveedores,
    }
    
    return render(request, 'proveedores.html', context)

@login_required
def reportes(request):
    return render(request, 'reportes.html')

@login_required
def alertas(request):
    alertas = Alerta.objects.filter(activa=True).select_related('producto')
    
    context = {
        'alertas': alertas,
    }
    
    return render(request, 'alertas.html', context)