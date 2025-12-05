from django.urls import path
from PaginaWeb import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventario/', views.inventario, name='inventario'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('reportes/', views.reportes, name='reportes'),
    path('unidades/', views.unidades_lista, name='unidades_lista'),
    path('unidades/nueva/', views.unidad_crear, name='unidad_crear'),
    path('unidades/editar/<int:id>/', views.unidad_editar, name='unidad_editar'),
    path('unidades/eliminar/<int:id>/', views.unidad_eliminar, name='unidad_eliminar'),
    path('productos/', views.productos_lista, name='productos_lista'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('productos/editar/<int:id>/', views.producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:id>/', views.producto_eliminar, name='producto_eliminar'),
    path('movimientos/', views.movimientos_lista, name='movimientos_lista'),
    path('movimientos/nuevo/', views.movimiento_crear, name='movimiento_crear'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('proveedores/nuevo/', views.proveedor_crear, name='proveedor_crear'),
    path('transportistas/', views.transportistas, name='transportistas'),
    path('transportistas/nuevo/', views.transportista_crear, name='transportista_crear'),
    path('proveedores/editar/<int:id>/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/eliminar/<int:id>/', views.proveedor_eliminar, name='proveedor_eliminar'),
    path("reportes/movimientos/excel/", views.reporte_movimientos_excel, name="reporte_movimientos_excel"),
    path("reportes/inventario/excel/", views.reporte_inventario_excel, name="reporte_inventario_excel"),
    path("reportes/proveedores/excel/", views.reporte_proveedores_excel, name="reporte_proveedores_excel"),
]
