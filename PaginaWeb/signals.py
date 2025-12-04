from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from .models import UnidadMedida

@receiver(post_migrate)
def crear_unidades(sender, **kwargs):
    # Verifica que la app correcta haya migrado
    if sender.label != "PaginaWeb":
        return

    unidades = [
        "Unidades",
        "Kilos",
        "Gramos",
        "Cajas",
        "Paquetes",
        "Bolsas",
        "Mallas",
    ]

    for u in unidades:
        UnidadMedida.objects.get_or_create(nombre=u)
