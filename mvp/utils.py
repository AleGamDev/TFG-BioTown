import string
import random
from . import models
from django.conf import settings
from paypalrestsdk import Payout, ResourceNotFound
import paypalrestsdk

def generador_numPedido(size=10, chars=string.ascii_uppercase + string.digits):
    numPedido = "".join(random.choice(chars) for x in range(size))
    try:
        pedido = models.Pedido.objects.get(numeroPedido=numPedido)
        generador_numPedido()
    except models.Pedido.DoesNotExist:
        return numPedido

def pagarProductores(datosProductores, numPedido):
    paypalrestsdk.configure({
        'mode': settings.PAYPAL_MODE, #sandbox or live
        'client_id': settings.PAYPAL_CLIENT_ID,
        'client_secret': settings.PAYPAL_CLIENT_SECRET
    })

    payout = Payout({
    "sender_batch_header": {
        "sender_batch_id": numPedido,
        "email_subject": "Tienes un pago"
    },
    "items": []
    })

    senderItemId = 1

    for email, cantidad in datosProductores.items():
        payout.items.append({
            "recipient_type": "EMAIL",
            "amount": {
                "value": cantidad,
                "currency": "EUR"
            },
            "receiver": email,
            "note": "Gracias por sus servicios.",
            "sender_item_id": "item_" + str(senderItemId)
        })
        senderItemId += 1

    if payout.create(sync_mode=False):
        print("Pago[%s] creado con éxito" %
            (payout.batch_header.payout_batch_id))
    else:
        print(payout.error)