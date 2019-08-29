from django.shortcuts import render, redirect
from django.views.generic.base import RedirectView
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth import authenticate, update_session_auth_hash
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from . import models
from . import forms
from django.conf import settings
from .utils import generador_numPedido, pagarProductores
from django.views.decorators.csrf import csrf_exempt

# Función vista para la página de inicio:
def index(request):
    noticiasBlog = models.Blog.objects.all().order_by('-fechaHora')[:4]
    context = {'noticiasBlog':noticiasBlog}
    return render(request, 'index.html', context)

def resultadoBusqueda(request):
    busqueda = request.GET.get('q')
    los_prods = models.Producto.objects.filter(
        Q(nombre__icontains=busqueda))
    total_productos = len(los_prods)

    page = request.GET.get('page', 1)
    paginator = Paginator(los_prods, 5) # Muestra 5 productos por pagina
    try:
        los_productos = paginator.page(page)
    except PageNotAnInteger:
        los_productos = paginator.page(1)
    except EmptyPage:
        los_productos = paginator.page(paginator.num_pages)

    context = {'busqueda': busqueda, 'los_productos': los_productos,
        'total_productos': total_productos}
    return render(request, 'resultadoBusqueda.html', context)

def login(request):
    if request.method == 'POST':
        formularioLogin = forms.LoginForm(data=request.POST)
        if formularioLogin.is_valid():
            user = formularioLogin.login(request)
            auth_login(request, user)
            return redirect('index')
        else:
            context = {'formularioLogin': formularioLogin}
            return render(request, './login.html', context)
    else:
        formularioLogin = forms.LoginForm()
    context = {'formularioLogin': formularioLogin}
    return render(request, './login.html', context)

@login_required
def cambiarContraseña(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            userPassCambiada = form.save()
            userPassCambiada.save()
            update_session_auth_hash(request, form.user)
            return redirect('perfil')
        else:
            context = {'cambiarPass_form': form}
            return render(request, './cambiarContraseña.html', context)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, './cambiarContraseña.html', {'cambiarPass_form': form})

def cerrarSesion(request):
    logout(request)
    return redirect('index')

def nuevoAdmin(request):
    if request.method == "POST":
        form = forms.AdminForm(request.POST)
        if form.is_valid():
            nuevo_admin = form.save()
            nuevo_admin.save()
            return redirect('login')
    else:
        form = forms.AdminForm()
    return render(request, './registroAdmin.html', {'admin_form': form})

def nuevoConsumidor(request):
    if request.method == "POST":
        form = forms.ConsumidorForm(request.POST)
        if form.is_valid():
            nuevo_consumidor = form.save()
            nuevo_consumidor.save()
            return redirect('login')
    else:
        form = forms.ConsumidorForm()
    return render(request, './registroConsumidor.html', {'consumidor_form': form})

@login_required
def editarConsumidor(request):
    consumidor = models.Consumidor.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = forms.EditarConsumidorForm(request.POST, instance=consumidor)
        if form.is_valid():
            consumidor_editado = form.save()
            consumidor_editado.save()
            return redirect('perfil')
        else:
            context = {'editarConsumidor_form': form}
            return render(request, './editarConsumidor.html', context)
    else:
        form = forms.EditarConsumidorForm(instance=consumidor)
    return render(request, './editarConsumidor.html', {'editarConsumidor_form': form})

def nuevoProductor(request):
    if request.method == "POST":
        form = forms.ProductorForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_productor = form.save()
            nuevo_productor.save()
            return redirect('login')
    else:
        form = forms.ProductorForm()
    return render(request, './registroProductor.html', {'productor_form': form})

@login_required
def editarProductor(request):
    productor = models.Productor.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = forms.EditarProductorForm(request.POST, request.FILES, instance=productor)
        if form.is_valid():
            productor_editado = form.save()
            productor_editado.save()
            return redirect('perfil')
        else:
            context = {'editarProductor_form': form}
            return render(request, './editarProductor.html', context)
    else:
        form = forms.EditarProductorForm(instance=productor)
    return render(request, './editarProductor.html', {'editarProductor_form': form})

def infoProductor(request, productor_id):
    productor = get_object_or_404(models.Productor, pk=productor_id)
    # El servicio de recogida, geolocalizacion, cobro y reseñas del productor
    recogidaProductor = models.TipoRecogida.objects.filter(productor_id=productor_id)
    geolocalizacion = models.Geolocalizacion.objects.filter(productor_id=productor_id)
    cobroProductor = models.FormaCobro.objects.filter(productor_id=productor_id)
    reseniasProductor = models.ReseñaProductor.objects.filter(productor_id=productor_id).order_by('fechaHora')[:9]
    # El POST para agregar las reseñas, solo para CONSUMIDORES:
    if request.method == "POST":
        form = forms.ReseñaProductorForm(request.POST)
        if form.is_valid():
            reseñaProductor = form.save(commit=False)
            reseñaProductor.fechaHora = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
            reseñaProductor.productor = models.Productor.objects.get(id=productor_id)
            reseñaProductor.consumidor = models.Consumidor.objects.get(id=request.user.id)
            reseñaProductor.save()
            return redirect('infoProductor', productor_id=productor.pk)
    else:
        form = forms.ReseñaProductorForm()
    context = {'productor': productor, 'recogidaProductor': recogidaProductor,
        'geolocalizacion': geolocalizacion,'cobroProductor': cobroProductor,
        'reseniasProductor': reseniasProductor, 'resProductor_form': form}
    return render(request, './infoProductor.html', context)

def verProductos(request, productor_id):
    productor = get_object_or_404(models.Productor, pk=productor_id)
    los_prods = models.Producto.objects.filter(productor_id=productor_id).order_by('nombre')
    total_productos = models.Producto.objects.all().filter(productor_id=productor_id).count()

    page = request.GET.get('page', 1)
    paginator = Paginator(los_prods, 5) # Muestra 5 productores del productor por pagina
    try:
        los_productos = paginator.page(page)
    except PageNotAnInteger:
        los_productos = paginator.page(1)
    except EmptyPage:
        los_productos = paginator.page(paginator.num_pages)

    context = {'productor':productor, 'los_productos':los_productos, 'total_productos':total_productos}
    return render(request, 'verProductos.html', context)

@login_required
def añadirProducto(request):
    productor = models.Productor.objects.get(id=request.user.id)
    if request.method == "POST":
        form = forms.ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.productor = productor
            producto.save()
            return redirect('perfil')
    else:
        form = forms.ProductoForm()
    return render(request, './nuevoProducto.html', {'nuevoProducto_form': form})

@login_required
def editarProducto(request, producto_id):
    producto = get_object_or_404(models.Producto, pk=producto_id)
    if request.method == "POST":
        form = forms.EditarProductoForm(request.POST, request.FILES, instance=producto)
        if (form.is_valid() and producto.productor.id == request.user.id):
            producto_editado = form.save()
            producto_editado.save()
            return redirect('perfil')
        else:
            context = {'editarProducto_form': form}
            return render(request, './editarProducto.html', context)
    else:
        form = forms.EditarProductoForm(instance=producto)
    return render(request, './editarProducto.html', {'producto': producto, 'editarProducto_form': form})

@login_required
def borrarProducto(request, producto_id):
    producto = get_object_or_404(models.Producto, pk=producto_id)
    if (producto.productor.id == request.user.id):
        producto.delete()
    return redirect('perfil')

def infoProducto(request, producto_id):
    producto = get_object_or_404(models.Producto, pk=producto_id)
    # Reseñas del producto
    reseniasProducto = models.ReseñaProducto.objects.filter(producto_id=producto_id).order_by('fechaHora')[:9]
    # El POST para agregar las reseñas, solo para CONSUMIDORES:
    if request.method == "POST":
        form = forms.ReseñaProductoForm(request.POST)
        if form.is_valid():
            reseñaProducto = form.save(commit=False)
            reseñaProducto.fechaHora = datetime.today().strftime('%d-%m-%Y-%H:%M:%S')
            reseñaProducto.producto = models.Producto.objects.get(id=producto_id)
            reseñaProducto.consumidor = models.Consumidor.objects.get(id=request.user.id)
            reseñaProducto.save()
            return redirect('infoProducto', producto_id=producto.pk)
    else:
        form = forms.ReseñaProductoForm()
    context = {'producto': producto, 'reseniasProducto': reseniasProducto, 'resProducto_form': form}
    return render(request, './infoProducto.html', context)

@login_required
def verPedido(request, pedido_id):
    pedido = models.Pedido.objects.get(id=pedido_id, consumidor_id=request.user.id)
    carritoId = pedido.carrito_id
    carrito = models.Carrito.objects.get(id=carritoId)
    items = models.ItemCarrito.objects.filter(carrito_id=carritoId)
    productores = models.PedidoAProductor.objects.filter(pedido_id=pedido.id)
    context = {'pedido':pedido, 'carrito':carrito, 'items':items, 'productores':productores}
    return render(request, './verPedido.html', context)

@login_required
def verPedidoProductor(request, pedido_id):
    pedidoProductor = models.PedidoAProductor.objects.get(pedido_id=pedido_id, productor_id=request.user.id)
    pedidoId = pedidoProductor.pedido_id
    pedido = models.Pedido.objects.get(id=pedidoId)
    carritoId = pedido.carrito_id
    carrito = models.Carrito.objects.get(id=carritoId)
    items = models.ItemCarrito.objects.filter(carrito_id=carritoId, productor_id=request.user.id)

    request.session['contar_pedidos'] = models.PedidoAProductor.objects.filter(
        Q(productor_id=request.user.id) & Q(visto=False)).count()
    contarPed = request.session['contar_pedidos']
    if (pedidoProductor.visto == False and pedidoProductor.productor_id == request.user.id):
        contarPed = contarPed - 1
        pedidoProductor.visto = True
        pedidoProductor.save()

    context = {'pedidoProductor':pedidoProductor, 'pedido':pedido, 'carrito':carrito, 'items':items}
    return render(request, './verPedidoProductor.html', context)

@login_required
def añadirRecogida(request):
    productor = models.Productor.objects.get(id=request.user.id)
    if request.method == "POST":
        form = forms.TipoRecogidaForm(request.POST)
        sub_form = forms.GeolocalizacionForm(request.POST)
        if form.is_valid() and sub_form.is_valid():
            recogida = form.save(commit=False)
            geo = sub_form.save(commit=False)
            geo.productor = productor
            recogida.productor = productor
            geo.save()
            recogida.save()
            return redirect('perfil')
    else:
        form = forms.TipoRecogidaForm()
        sub_form = forms.GeolocalizacionForm()
    context =  {'nuevaRecogida_form': form, 'nuevaGeo_form': sub_form}
    return render(request, './nuevaRecogida.html', context)

@login_required
def editarRecogida(request):
    recogida = models.TipoRecogida.objects.get(productor=request.user)
    if request.method == 'POST':
        form = forms.TipoRecogidaForm(request.POST, instance=recogida)
        if form.is_valid():
            recogida = form.save(commit=False)
            recogida.save()
            return redirect('perfil')
        else:
            context = {'editarRecogida_form': form}
            return render(request, './editarRecogida.html', context)
    else:
        form = forms.TipoRecogidaForm(instance=recogida)
    context =  {'editarRecogida_form': form}
    return render(request, './editarRecogida.html', context)

@login_required
def añadirFormaCobro(request):
    productor = models.Productor.objects.get(id=request.user.id)
    if request.method == "POST":
        form = forms.FormaCobroForm(request.POST)
        if form.is_valid():
            cobro = form.save(commit=False)
            cobro.productor = productor
            cobro.save()
            print(cobro.tipoCobro)
            return redirect('perfil')
    else:
        form = forms.FormaCobroForm()
    return render(request, './nuevaFormaCobro.html', {'nuevaFormaCobro_form': form})

@login_required
def editarFormaCobro(request):
    formaCobro = models.FormaCobro.objects.get(productor=request.user)
    if request.method == 'POST':
        form = forms.FormaCobroForm(request.POST, instance=formaCobro)
        if form.is_valid():
            formaCobro = form.save(commit=False)
            formaCobro.save()
            return redirect('perfil')
        else:
            context = {'editarFormaCobro_form': form, 'formaCobro': formaCobro}
            return render(request, './editarFormaCobro.html', context)
    else:
        form = forms.FormaCobroForm(instance=formaCobro)
    return render(request, './editarFormaCobro.html', {'editarFormaCobro_form': form, 'formaCobro': formaCobro})

@login_required
def añadirBlog(request):
    admin = models.Administrador.objects.get(id=request.user.id)
    if request.method == "POST":
        form = forms.BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.administrador = admin
            blog.save()
            return redirect('perfil')
    else:
        form = forms.BlogForm()
    return render(request, './nuevoBlog.html', {'nuevoBlog_form': form})

@login_required
def editarBlog(request, blog_id):
    blog = get_object_or_404(models.Blog, pk=blog_id)
    if request.method == "POST":
        form = forms.EditarBlogForm(request.POST, request.FILES, instance=blog)
        if (form.is_valid() and blog.administrador.id == request.user.id):
            blog_editado = form.save()
            blog_editado.save()
            return redirect('perfil')
        else:
            context = {'editarBlog_form': form}
            return render(request, './editarBlog.html', context)
    else:
        form = forms.EditarBlogForm(instance=blog)
    return render(request, './editarBlog.html', {'blog':blog, 'editarBlog_form':form})

@login_required
def borrarBlog(request, blog_id):
    blog = get_object_or_404(models.Blog, pk=blog_id)
    if (blog.administrador.id == request.user.id):
        blog.delete()
    return redirect('perfil')

def blog(request):
    noticias = models.Blog.objects.all().order_by('fechaHora')
    total_noticias = models.Blog.objects.all().count()

    page = request.GET.get('page', 1)
    paginator = Paginator(noticias, 5) # Muestra 5 noticias por pagina
    try:
        noticiasBlog = paginator.page(page)
    except PageNotAnInteger:
        noticiasBlog = paginator.page(1)
    except EmptyPage:
        noticiasBlog = paginator.page(paginator.num_pages)

    context = {'noticiasBlog':noticiasBlog, 'total_noticias':total_noticias}
    return render(request, 'blog.html', context)

def verNoticia(request, blog_id):
    blog = get_object_or_404(models.Blog, pk=blog_id)
    context = {'blog':blog}
    return render(request, 'verNoticia.html', context)

@login_required
def borrarUsuario(request, usuario_id):
    usuario = get_object_or_404(models.User, pk=usuario_id)
    admin = models.Administrador.objects.get(id=request.user.id)
    if (admin):
        usuario.delete()
    return redirect('perfil')

@login_required
def enviarMensaje(request, usuario_id):
    emisor = models.User.objects.get(id=request.user.id)
    receptor = models.User.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = forms.MensajeriaForm(request.POST)
        if form.is_valid():
            msn = form.save(commit=False)
            msn.receptor = receptor
            msn.emisor = emisor
            msn.save()
            return redirect('perfil')
        else:
            context = {'emisor':emisor, 'receptor': receptor, 'enviarMensaje_form': form}
            return render(request, './enviarMensaje.html', context)
    else:
        form = forms.MensajeriaForm()
    context = {'emisor':emisor, 'receptor': receptor, 'enviarMensaje_form': form}
    return render(request, './enviarMensaje.html', context)

@login_required
def verMensaje(request, mensaje_id):
    mensaje = get_object_or_404(models.Mensajeria, pk=mensaje_id)
    request.session['contar_mensajes'] = models.Mensajeria.objects.filter(
        Q(receptor_id=request.user.id) & Q(leido=False)).count()
    contar = request.session['contar_mensajes']
    if (mensaje.leido == False and mensaje.receptor_id == request.user.id):
        contar = contar - 1
        mensaje.leido = True
        mensaje.save()
    context = {'mensaje':mensaje}
    return render(request, 'verMensaje.html', context)

def catalogoProductores(request):
    total_productores = models.Productor.objects.all().count()
    geolocalizaciones = models.Geolocalizacion.objects.all()
    prods = models.Productor.objects.all().order_by('nombreEmpresa')

    page = request.GET.get('page', 1)
    paginator = Paginator(prods, 5) # Muestra 5 productores por pagina
    try:
        productores = paginator.page(page)
    except PageNotAnInteger:
        productores = paginator.page(1)
    except EmptyPage:
        productores = paginator.page(paginator.num_pages)

    context = {'productores': productores, 'total_productores': total_productores, 'geolocalizaciones': geolocalizaciones}
    return render(request, './catalogoProductores.html', context)

def catalogoProductos(request, tipo):
    prods = models.Producto.objects.filter(tipo=tipo).order_by('nombre')
    total_productos = len(prods)

    page = request.GET.get('page', 1)
    paginator = Paginator(prods, 5) # Muestra 5 productos por pagina
    try:
        productos = paginator.page(page)
    except PageNotAnInteger:
        productos = paginator.page(1)
    except EmptyPage:
        productos = paginator.page(paginator.num_pages)

    context = {'productos': productos, 'total_productos': total_productos, 'tipo': tipo}
    return render(request, './catalogoProductos.html', context)

@login_required
def carroCompra(request):
    consumidor = models.Consumidor.objects.get(id=request.user.id)
    try:
        carritoId = request.session['carrito_id']
        carrito = models.Carrito.objects.get(id=carritoId)
    except:
        carritoId = None

    if carritoId:
        context = {'consumidor':consumidor, 'carrito': carrito}
    else:
        context = {'consumidor':consumidor, 'empty': True}
    return render(request, './carroCompra.html', context)

@login_required
def actualizaCarro(request, producto_id):
    request.session.set_expiry(60000) # Tiene 16 horas para que se cierre la sesion
    try:
        cant = request.GET.get('cant')
        update_cant = True
    except:
        cant = None
        update_cant = False

    try:
        carritoId = request.session['carrito_id']
    except:
        nuevoCarrito = models.Carrito()
        nuevoCarrito.save()
        request.session['carrito_id'] = nuevoCarrito.pk
        carritoId = nuevoCarrito.pk

    carrito = models.Carrito.objects.get(id=carritoId)
    producto = get_object_or_404(models.Producto, pk=producto_id)
    productor = models.Productor.objects.get(id=producto.productor_id)
    item_carrito, created = models.ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto, productor=productor)
    if created:
        print ("Yeah")

    if update_cant and cant:
        if int(cant) == 0:
            item_carrito.delete()
        else:
            item_carrito.cantidad = cant
            item_carrito.save()
    else:
        pass

    nuevo_total = 0.00
    for item in carrito.itemcarrito_set.all():
        linea_total = float(item.producto.precioUnidad) * item.cantidad
        nuevo_total += linea_total

    request.session['total_items'] = carrito.itemcarrito_set.count()
    carrito.total = nuevo_total
    carrito.save()

    productos = models.ItemCarrito.objects.filter(carrito_id=carritoId)
    for prod in productos:
        precio = float(prod.producto.precioUnidad) * prod.cantidad
        prod.precioTotal = precio
        if int(prod.cantidad) == 0:
            prod.delete()
        prod.save()

    return redirect('carroCompra')

@login_required
def infoPedido(request):
    consumidor = models.Consumidor.objects.get(id=request.user.id)
    try:
        carritoId = request.session['carrito_id']
        carrito = models.Carrito.objects.get(id=carritoId)
    except:
        carritoId = None
        return redirect('carroCompra')

    items = models.ItemCarrito.objects.filter(carrito_id=carritoId)
    productores = []
    # Productor de cada producto del carrito
    for item in items:
        productorId = item.productor_id
        productor = models.Productor.objects.get(id=productorId)
        if productores.count(productor) > 0:
            pass
        else:
            productores.append(productor)

    try:
        nuevo_pedido = models.Pedido.objects.get(carrito=carrito)
    except models.Pedido.DoesNotExist:
        nuevo_pedido = models.Pedido()
        nuevo_pedido.carrito = carrito
        nuevo_pedido.consumidor = consumidor
        nuevo_pedido.numeroPedido = generador_numPedido()
        # El nuevo_pedido.estado se autoañade a: "EnProceso"
        nuevo_pedido.save()
    except:
        return redirect('carroCompra')

    context = {'consumidor':consumidor, 'carrito':carrito, 'pedido':nuevo_pedido,
        'items':items, 'productores':productores}

    return render(request, 'infoPedido.html', context)

@login_required
@csrf_exempt
def pagar(request, pedido_id):
    print(request.body)

    pedido = models.Pedido.objects.get(id=pedido_id)
    carritoId = request.session['carrito_id']
    items = models.ItemCarrito.objects.filter(carrito_id=carritoId)

    productores = []
    # Productor de cada producto del carrito
    for item in items:
        productorId = item.productor_id
        productor = models.Productor.objects.get(id=productorId)
        if productores.count(productor) > 0:
            pass
        else:
            productores.append(productor)

    datosProductores = {}

    for productor in productores:
        p = productor.id
        pedidoAProductor = models.PedidoAProductor()
        pedidoAProductor.productor = productor
        pedidoAProductor.pedido = pedido
        gananciaProductor = 0.00
        for item in items:
            if (item.productor_id == p):
                gananciaProductor += float(item.precioTotal)
        pedidoAProductor.total = gananciaProductor
        datosProductores[productor.email] = gananciaProductor
        pedidoAProductor.save()

    if pedido.estado == 'EnProceso':
        pedido.estado = 'Realizado'
        pedido.save()

    pagarProductores(datosProductores, pedido.numeroPedido)

    return HttpResponse('OK')

def pagarConfirmado(request, pedido_id):
    pedido = models.Pedido.objects.get(id=pedido_id)

    del request.session['carrito_id']
    del request.session['total_items']

    context = {'pedido': pedido}
    return render(request, 'pagar.html', context)

@login_required
def perfil(request):
    # Los productos del productor logueado
    mis_productos = models.Producto.objects.filter(productor_id=request.user.id).order_by('nombre')
    # El servicio de recogida del productor logueado
    recogida_user = models.TipoRecogida.objects.filter(productor_id=request.user.id)
    geolocalizacion = models.Geolocalizacion.objects.filter(productor_id=request.user.id)
    # El blog del admin logueado
    mis_blogs = models.Blog.objects.filter(administrador_id=request.user.id).order_by('-fechaHora')
    # Todos los usuarios del sistema, para el admin
    los_usuarios = models.User.objects.all()
    # Los mensajes de los usuarios
    mis_mensajes = models.Mensajeria.objects.filter(
        Q(emisor_id=request.user.id) | Q(receptor_id=request.user.id)).order_by('-fechaHora')
    # La sesion de los mensajes sin leer de los usuarios
    request.session['contar_mensajes'] = models.Mensajeria.objects.filter(
        Q(receptor_id=request.user.id) & Q(leido=False)).count()
    # Pedidos de los consumidores
    mis_pedidos = models.Pedido.objects.filter(consumidor_id=request.user.id).order_by('-fechaHora')
    # Los pedidos del productor
    pedidosProductor = models.PedidoAProductor.objects.filter(productor_id=request.user.id).order_by('-fechaHora')
    # La sesion de los pedidos sin ver de los productores
    request.session['contar_pedidos'] = models.PedidoAProductor.objects.filter(
        Q(productor_id=request.user.id) & Q(visto=False)).count()

    context = {'mis_productos':mis_productos, 'recogida_user':recogida_user, 'geolocalizacion':geolocalizacion,
    'mis_blogs':mis_blogs, 'los_usuarios':los_usuarios, 'mis_mensajes':mis_mensajes, 'mis_pedidos':mis_pedidos,
    'pedidosProductor':pedidosProductor}
    return render(request, './perfil.html', context)

def terminosYCondiciones(request):
    return render(request, './TyC.html')

def politicasDePrivacidad(request):
    return render(request, './PdP.html')

