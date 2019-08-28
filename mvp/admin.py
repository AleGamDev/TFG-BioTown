from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Administrador)
admin.site.register(Consumidor)
admin.site.register(Productor)
admin.site.register(Mensajeria)
admin.site.register(Producto)
admin.site.register(FormaCobro)
admin.site.register(ReseñaProductor)
admin.site.register(ReseñaProducto)
admin.site.register(Pedido)
admin.site.register(PedidoAProductor)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)