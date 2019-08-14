"""bioTown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path
from mvp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('login', views.login, name='login'),
    path('cambiarContraseña', views.cambiarContraseña, name='cambiarContraseña'),
    path('cerrarSesion', views.cerrarSesion, name='logout'),
    path('resultadoBusqueda/', views.resultadoBusqueda, name='resultadoBusqueda'),
    path('nuevoConsumidor', views.nuevoConsumidor, name='nuevoConsumidor'),
    path('nuevoAdmin', views.nuevoAdmin, name='nuevoAdmin'),
    path('editarConsumidor', views.editarConsumidor, name='editarConsumidor'),
    path('nuevoProductor', views.nuevoProductor, name='nuevoProductor'),
    path('editarProductor', views.editarProductor, name='editarProductor'),
    path('infoProductor/<productor_id>/', views.infoProductor, name='infoProductor'),
    path('infoProductor/verProductos/<productor_id>', views.verProductos, name='verProductos'),
    path('nuevoProducto', views.añadirProducto, name='nuevoProducto'),
    path('borrarProducto/<producto_id>/', views.borrarProducto, name='borrarProducto'),
    path('editarProducto/<producto_id>/', views.editarProducto, name='editarProducto'),
    path('infoProducto/<producto_id>/', views.infoProducto, name='infoProducto'),
    path('nuevaRecogida', views.añadirRecogida, name='nuevaRecogida'),
    path('editarRecogida', views.editarRecogida, name='editarRecogida'),
    path('nuevoReparto', views.añadirReparto, name='nuevoReparto'),
    path('editarReparto', views.editarReparto, name='editarReparto'),
    path('nuevaFormaCobro', views.añadirFormaCobro, name='nuevaFormaCobro'),
    path('editarFormaCobro', views.editarFormaCobro, name='editarFormaCobro'),
    path('nuevoBlog', views.añadirBlog, name='nuevoBlog'),
    path('editarBlog/<blog_id>/', views.editarBlog, name='editarBlog'),
    path('borrarBlog/<blog_id>/', views.borrarBlog, name='borrarBlog'),
    path('blog', views.blog, name='blog'),
    path('verNoticia/<blog_id>/', views.verNoticia, name='verNoticia'),
    path('enviarMensaje/<usuario_id>/', views.enviarMensaje, name='enviarMensaje'),
    path('verMensaje/<mensaje_id>/', views.verMensaje, name='verMensaje'),
    path('borrarUsuario/<usuario_id>/', views.borrarUsuario, name='borrarUsuario'),
    path('catalogoProductores', views.catalogoProductores, name='catalogoProductores'),
    path('catalogoProductos/<tipo>/', views.catalogoProductos, name='catalogoProductos'),
    path('carroCompra', views.carroCompra, name='carroCompra'),
    path('actualizaCarro/<producto_id>/', views.actualizaCarro, name='actualizaCarro'),
    path('perfil', views.perfil, name='perfil'),
    path('TyC', views.terminosYCondiciones, name='terminosYCondiciones'),
    path('PdP', views.politicasDePrivacidad, name='politicasDePrivacidad'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)