from django.urls import path
from PaginaWeb import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('inventario/', views.inventario, name='inventario'),
    path('productos/', views.productos, name='productos'),
    path('movimientos/', views.movimientos, name='movimientos'),
    path('proveedores/', views.proveedores, name='proveedores'),
    path('reportes/', views.reportes, name='reportes'),
    
]
