from django.db import models
from django.contrib.auth.models import User
from django.apps import AppConfig


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Unidad de Medida"
        verbose_name_plural = "Unidades de Medida"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    unidad_base = models.ForeignKey(
        UnidadMedida,
        on_delete=models.PROTECT,
        related_name="productos_base"
    )
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def estado(self):
        if self.stock_actual <= 0:
            return "agotado"
        if self.stock_actual < self.stock_minimo:
            return "critico"
        umbral_normal = self.stock_minimo + (self.stock_minimo / 2)
        if self.stock_actual < umbral_normal:
            return "bajo"
        return "normal"


class Transportista(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    patente = models.CharField(max_length=20, blank=True, null=True)
    empresa = models.CharField(max_length=150, blank=True, null=True)
    region = models.CharField(max_length=120, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        etiqueta = self.nombre
        if self.patente:
            etiqueta += f" ({self.patente})"
        return etiqueta

    
class Movimiento(models.Model):
    TIPOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('merma', 'Merma'),
        ('ajuste', 'Ajuste'),
    ]

    producto = models.ForeignKey(Producto,null=True,blank=True,on_delete=models.SET_NULL)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    unidad_ingreso = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name="mov_unidad_ingreso")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    factor = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    motivo = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"


class Alerta(models.Model):
    TIPOS_ALERTA = [
        ('stock_bajo', 'Stock Bajo'),
        ('stock_critico', 'Stock Crítico'),
        ('vencimiento', 'Próximo a Vencer'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=20, choices=TIPOS_ALERTA)
    mensaje = models.TextField()
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"


class PaginawebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PaginaWeb'

    def ready(self):
        import PaginaWeb.signals
