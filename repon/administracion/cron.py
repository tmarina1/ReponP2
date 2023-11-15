from django.utils import timezone
from datetime import timedelta
from inventario.models import Insumo
from django.core.mail import EmailMessage
from repon.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from django.db.models import Q

def verificacionFechas():        
    fechaActual = timezone.now()
    objetosAVencerse = Insumo.objects.filter(
        Q(fechaCaducidad__lte=fechaActual + timedelta(days=40)) &
        Q(correoVencimiento=False)
    )
    for objeto in objetosAVencerse:
        mensaje = f'El insumo con referencia "{objeto.referencia}" con codigo "{objeto.codigo}" se vence en "{objeto.fechaCaducidad}" (en 40 días) para que lo tengas presente \n ¡Gracias por usar nuestro sitio PAS! \n Atentamente el equipo de petacos.'
        msg = EmailMessage(f'Notificación de caducidad insumo', mensaje,
                    EMAIL_HOST_USER, [objeto.proyectoAsociado.coordinadorVinculado.usuario.email])
        msg.send()
        objeto.correoVencimiento = True
        objeto.save()

def verificacionFechas1():
    fechaActual = timezone.now()
    objetosAVencerse = Insumo.objects.filter(
        Q(fechaIngreso__lt=fechaActual - timedelta(days=40)) &
        Q(correoFechaIngreso=False)
    )
    for objeto in objetosAVencerse:
        mensaje = f'El insumo con referencia "{objeto.referencia}" con codigo "{objeto.codigo}" fue ingresado en la fecha "{objeto.fechaIngreso}" para que tengas presente utilizarlo o gestionarlo \n ¡Gracias por usar nuestro sitio PAS! \n Atentamente el equipo de petacos.'
        msg = EmailMessage(f'Notificación de longevidad del insumo', mensaje,
                    EMAIL_HOST_USER, [objeto.proyectoAsociado.coordinadorVinculado.usuario.email])
        msg.send()
        objeto.correoFechaIngreso = True
        objeto.save()