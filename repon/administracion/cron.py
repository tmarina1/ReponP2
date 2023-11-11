from django.utils import timezone
from datetime import timedelta
from inventario.models import Insumo
from django.core.mail import send_mail
from repon.settings import EMAIL_HOST_USER

def verificacionFechas():
    fechaActual = timezone.now()
    objetosAVencerse = Insumo.objects.filter(fechaCaducidad__lte = fechaActual + timedelta(days=40))
    for objeto in objetosAVencerse:
        mensaje = f'El insumo con referencia "{objeto.referencia}" con codigo "{objeto.codigo}" se vence en "{objeto.fechaCaducidad}" (en 40 días) para que lo tengas presente \n ¡Gracias por usar nuestro sitio PAS! \n Atentamente el equipo de petacos.'
        send_mail('Advertencia de Caducidad de Insumo', mensaje, EMAIL_HOST_USER , [objeto.proyectoAsociado.coordinadorVinculado.usuario.email])
