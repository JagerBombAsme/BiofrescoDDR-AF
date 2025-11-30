from django.db import models
from django.contrib.auth.models import User

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

class Producto(models.Model):
    UNIDADES_MEDIDA = [
        ('unidad', 'Unidades'),
        ('kg', 'Kilogramos'),
        ('caja', 'Cajas'),
        ('manojo', 'Manojos'),
        ('bolsa', 'Bolsas'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    unidad_medida = models.CharField(max_length=20, choices=UNIDADES_MEDIDA)
    factor_conversion = models.IntegerField(default=1, help_text="Ej: 18 unidades por caja")
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    vida_util_dias = models.IntegerField(blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def stock_estado(self):
        if self.stock_actual == 0:
            return 'agotado'
        elif self.stock_actual < self.stock_minimo:
            return 'critico'
        elif self.stock_actual < (self.stock_minimo * 1.5):
            return 'bajo'
        return 'normal'

class Movimiento(models.Model):
    TIPOS_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('merma', 'Merma'),
        ('ajuste', 'Ajuste'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"
    
    def save(self, *args, **kwargs):
        # Actualizar stock automáticamente
        if self.tipo == 'entrada':
            self.producto.stock_actual += self.cantidad
        elif self.tipo in ['salida', 'merma']:
            self.producto.stock_actual -= self.cantidad
        
        self.producto.save()
        super().save(*args, **kwargs)

class Alerta(models.Model):
    TIPOS_ALERTA = [
        ('stock_bajo', 'Stock Bajo'),
        ('stock_critico', 'Stock Crítico'),
        ('vencimiento', 'Próximo a Vencer'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS_ALERTA)
    mensaje = models.TextField()
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre}"