from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError 
import datetime
 
"""class ValidateFechaLlegada(object):

    def __init__(self, fechaSalida):
        self.fechaSalida=str(fechaSalida)
        
    def __call__(self,fechaSalida):
        if str(self.date()) <= datetime.date.today() or self.date()<self.fechaSalida:
            raise ValidationError(
            _('%(fecha)s no es valida'),
            params={'fecha': fecha},
            )"""


def validatePrecio(precio):
        if precio<0:
            raise ValidationError(
            _('Por favor ingrese un precio mayor a 0'),
            params={'precio': precio},
            )
        else:
            return precio

def validateFechaSalida(fecha):
        print (datetime.datetime.now())
        if fecha.now() < datetime.datetime.now():
            raise ValidationError(
            _('%(fecha)s no es valida'),
            params={'fecha': fecha},
            )