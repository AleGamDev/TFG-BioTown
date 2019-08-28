from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField
from datetime import datetime, timedelta
from django.db import models

def fotoLogo_directory_path(instance, filename):
    # El archivo se subirá a: MEDIA_ROOT/<user_id>/<filename>
    return 'fotoLogo/{0}'.format(filename)

def fotoProductos_directory_path(instance, filename):
    # El archivo se subirá a: MEDIA_ROOT/<user_id>/<filename>
    return 'fotoProductos/{0}'.format(filename)

def fotoBlog_directory_path(instance, filename):
    # El archivo se subirá a: MEDIA_ROOT/<user_id>/<filename>
    return 'fotoBlog/{0}'.format(filename)

class User(AbstractUser):
    email = models.EmailField('Email', unique = True)
    nombre = models.CharField('Nombre', max_length=25)
    apellidos = models.CharField('Apellidos', max_length=100)
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)

class Administrador(User):
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)

class Consumidor(User):
    def __str__(self):
        return '%s %s' % (self.nombre, self.apellidos)

class Productor(User):
    nombreEmpresa = models.CharField('Nombre de empresa', max_length=50)
    descripcion = models.TextField('Descripción', help_text='Describe tu empresa', max_length=500)
    telefono = models.CharField('Teléfono', max_length=9)
    fotoLogo = models.FileField('Logo', null=True, blank=True, upload_to=fotoLogo_directory_path)
    def __str__(self):
        return '%s' % (self.nombreEmpresa)

class Producto(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    foto = models.FileField('Foto', null=True, blank=True, upload_to=fotoProductos_directory_path)
    opcionesTipoProducto = (
        ('Verduras', 'Verduras'),
        ('Frutas', 'Frutas'),
        ('Panadería y bollería', 'Panadería y bollería'),
        ('Legumbres', 'Legumbres'),
        ('Pastas y arroces', 'Pastas y arroces'),
        ('Harinas, cereales y semillas', 'Harinas, cereales y semillas'),
        ('Frutos secos y deshidratados', 'Frutos secos y deshidratados'),
        ('Lácteos, yogures y huevos', 'Lácteos, yogures y huevos'),
        ('Aceites, condimentos y sal', 'Aceites, condimentos y sal'),
        ('Azúcar y miel', 'Azúcar y miel'),
        ('Conservas y mermeladas', 'Conservas y mermeladas'),
        ('Zumos, cafés y bebidas', 'Zumos, cafés y bebidas'),
        ('Infusiones, tés y aromáticas', 'Infusiones, tés y aromáticas'),
        ('Vinos, cervezas y licores', 'Vinos, cervezas y licores'),
        ('Chocolate, aperitivos y dulces', 'Chocolate, aperitivos y dulces'),
        ('Higiene personal', 'Higiene personal'),
        ('Productos de limpieza', 'Productos de limpieza'),
        ('Alimentación infantil', 'Alimentación infantil'),
        ('Ropa y textil', 'Ropa y textil'),
    )
    tipo = models.CharField('Tipo de producto', max_length=30, choices=opcionesTipoProducto)
    opcionesCertificacionProducto = (
        ('Ecológico', 'Ecológico'),
        ('Kilómetro cero', 'Kilómetro cero'),
    )
    certificacion = models.CharField('Certificación', max_length=15, choices=opcionesCertificacionProducto)
    precioUnidad = models.DecimalField('Precio', validators=[MinValueValidator(0.00)], max_digits=8, decimal_places=2) # 999,999.99
    opcionesUnidadMedida = (
        ('€/Kg.','€/Kg.'),
        ('€/250gr.','€/250gr.'),
        ('€/500gr.','€/500gr.'),
        ('€/Ud.','€/Ud.'),
        ('€/Manojo','€/Manojo'),
        ('€/l.','€/l.'),
        ('€/250ml.','€/250ml.'),
        ('€/500ml.','€/500ml.'),
    )
    unidadMedida = models.CharField('Unidad de medida', max_length=10, choices=opcionesUnidadMedida)
    opcionesStock = (
        ('Sí', 'Sí'),
        ('No', 'No'),
    )
    stock = models.CharField('Stock', max_length=2, default='Sí', choices=opcionesStock)
    infoAdicional = models.TextField('Descripción', help_text='Describe el producto', max_length=500, blank=True, null=True)
    productor = models.ForeignKey(
        Productor, on_delete=models.CASCADE, related_name="productos")
    def __str__(self):
        return '%s %s %s' % (self.nombre, self.tipo, self.productor)

# Sistema de Reseña: Un Consumidor califica y comenta un Productor
class ReseñaProductor(models.Model):
    fechaHora = models.DateTimeField('Fecha y hora', auto_now_add = True)
    opcionesCalificacionProductor = (
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    )
    calificacion = models.CharField('Calificación', max_length=1, default='1', choices=opcionesCalificacionProductor)
    comentario = models.TextField('Comentario', help_text='Escriba su comentario', max_length=200)
    productor = models.ForeignKey(
        Productor, on_delete=models.CASCADE, related_name="reseñasProductor")
    consumidor = models.ForeignKey(
        Consumidor, on_delete=models.CASCADE, related_name="reseñasConsumidor")
    def __str__(self):
        return '%s %s' % (self.fechaHora, self.comentario)

# Sistema de Reseña: Un Consumidor califica y comenta un Producto
class ReseñaProducto(models.Model):
    fechaHora = models.DateTimeField('Fecha y hora', auto_now_add = True)
    opcionesCalificacionProducto = (
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    )
    calificacion = models.CharField('Calificación', max_length=1, default='1', choices=opcionesCalificacionProducto)
    comentario = models.TextField('Comentario', help_text='Escriba su comentario', max_length=200)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="reseñasProducto")
    consumidor = models.ForeignKey(
        Consumidor, on_delete=models.CASCADE, related_name="reseñasProducto")
    def __str__(self):
        return '%s %s' % (self.fechaHora, self.comentario)

# Sistema de Blog: sólo los admins pueden escribir noticias en el blog
class Blog(models.Model):
    titulo = models.CharField('Título', max_length=150)
    fechaHora = models.DateTimeField('Fecha y hora', auto_now_add = True)
    articulo = models.TextField('Artículo', help_text='Escriba el artículo', max_length=5000)
    foto = models.FileField('Foto', null=True, blank=True, upload_to=fotoBlog_directory_path)
    administrador = models.ForeignKey(
        Administrador, on_delete=models.CASCADE, related_name="blogs")
    def __str__(self):
        return '%s %s' % (self.titulo, self.fechaHora)

class Mensajeria(models.Model):
    titulo = models.CharField('Título', max_length=50)
    fechaHora = models.DateTimeField('Fecha', auto_now_add = True)
    comentario = models.TextField('Comentario', max_length=500)
    leido = models.BooleanField('Leído', default=False)
    emisor = models.ForeignKey(
        User, related_name='mensajesEnviados', on_delete=models.CASCADE)
    receptor = models.ForeignKey(
        User, related_name='mensajesRecibidos', on_delete=models.CASCADE)
    def __str__(self):
        return '%s %s %s' % (self.titulo, self.emisor, self.receptor)

class TipoRecogida(models.Model):
    direccion = models.TextField('Dirección', max_length=100)
    diasYHoras = models.TextField('Días y horas de recogida',
        help_text='Escriba los días y horas de recogida. Por ejemplo: L --> 10:30 a 14:30, M --> 9:00 a 17:30', max_length=500)
    productor = models.ForeignKey(
        Productor, on_delete=models.CASCADE, related_name="tiporecogida")
    def __str__(self):
        return '%s %s %s' % (self.diasYHoras, self.direccion, self.productor)

class Geolocalizacion(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    productor = models.ForeignKey(
        Productor, on_delete=models.CASCADE, related_name="geolocalizacion")
    def __str__(self):
        return '%s %s %s' % (self.latitud, self.longitud, self.productor)

class FormaCobro(models.Model):
    opcionesTipoCobro = (
        ('Efectivo', 'Efectivo'),
        ('Tarjeta de credito', 'Tarjeta de crédito'),
        ('Contra reembolso', 'Contra reembolso'),
    )
    tipoCobro = MultiSelectField(choices=opcionesTipoCobro, max_choices=3, max_length=60)
    productor = models.ForeignKey(
        Productor, on_delete=models.CASCADE, related_name="formaCobro")
    def __str__(self):
        return '%s %s' % (self.tipoCobro, self.productor)

class Carrito(models.Model):
    total = models.DecimalField('Total', validators=[MinValueValidator(0.00)], max_digits=8, decimal_places=2, default=0.00) # 999,999.99
    def __unicode__(self):
        return "Carrito total: %s" % (self.total)

class ItemCarrito(models.Model):
    cantidad = models.IntegerField('Cantidad', default=1)
    precioTotal = models.DecimalField('PrecioTotal', validators=[MinValueValidator(0.00)], max_digits=8, decimal_places=2, default=0.00) # 999,999.99
    carrito = models.ForeignKey(Carrito, null=True, blank=True, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    productor = models.ForeignKey(Productor, null=True, blank=True, on_delete=models.CASCADE)

class Pedido(models.Model):
    opcionesEstadoPedido = (
        ('EnProceso', 'En proceso'),
        ('Realizado', 'Realizado'),
        ('Cancelado', 'Cancelado'),
    )
    numeroPedido = models.CharField(max_length=25, unique=True)
    consumidor = models.ForeignKey(
        Consumidor, on_delete=models.CASCADE, related_name="pedidosConsumidor", null=True, blank=True)
    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE, related_name="carritoPedido")
    estado = models.CharField('Estado del pedido', max_length=20, choices=opcionesEstadoPedido, default='EnProceso')
    fechaHora = models.DateTimeField('Fecha y hora', auto_now_add = True)

class PedidoAProductor(models.Model):
    productor = models.ForeignKey(
        Productor, on_delete=models.CASCADE, null=True, blank=True)
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, null=True, blank=True)
    fechaHora = models.DateTimeField('Fecha y hora', auto_now_add = True)
    visto = models.BooleanField('Visto', default=False)
    total = models.DecimalField('Total', validators=[MinValueValidator(0.00)], max_digits=8, decimal_places=2, default=0.00) # 999,999.99

class Pago(models.Model):
    precioTotal = models.DecimalField('Total', validators=[MinValueValidator(0.00)], max_digits=8, decimal_places=2, default=0.00) # 999,999.99
    paypalId = models.CharField(max_length=100, null=True)
    fechaHora = models.DateTimeField('Fecha y hora', auto_now_add = True)
    consumidor = models.ForeignKey(Consumidor, on_delete=models.CASCADE, null=True, blank=True)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)