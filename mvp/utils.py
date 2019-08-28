import string
import random
from . import models

def generador_numPedido(size=10, chars=string.ascii_uppercase + string.digits):
    numPedido = "".join(random.choice(chars) for x in range(size))
    try:
        pedido = models.Pedido.objects.get(numeroPedido=numPedido)
        generador_numPedido()
    except models.Pedido.DoesNotExist:
        return numPedido