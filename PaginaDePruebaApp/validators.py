from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError 
import datetime

def validatePrecio(precio):
        if precio<0:
            raise ValidationError(
            _('Por favor ingrese un precio mayor a 0'),
            params={'precio': precio},
            )
        else:
            return precio
