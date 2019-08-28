from django import forms
from django.forms import ModelForm, Textarea
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
from django.template.defaultfilters import filesizeformat
from django.contrib.auth.forms import *
from django.conf import settings
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

class AdminForm(UserCreationForm):
    class Meta:
        model = models.Administrador
        fields = ('email', 'username', 'nombre', 'apellidos')

class ConsumidorForm(UserCreationForm):
    class Meta:
        model = models.Consumidor
        fields = ('email', 'username', 'nombre', 'apellidos')

class EditarConsumidorForm(UserChangeForm):
    class Meta:
        model = models.Consumidor
        fields = ('email', 'nombre', 'apellidos')

class ProductorForm(UserCreationForm):
    def clean_FotoLogo(self):
        content = self.cleaned_data['fotoLogo']
        return validarImagen(content)

    class Meta:
        model = models.Productor
        fields = ('email', 'username', 'nombre', 'apellidos', 'nombreEmpresa', 'descripcion', 'telefono', 'fotoLogo')

class EditarProductorForm(UserChangeForm):
    def clean_FotoLogo(self):
        content = self.cleaned_data['fotoLogo']
        return validarImagen(content)

    class Meta:
        model = models.Productor
        fields = ('email', 'nombre', 'apellidos', 'nombreEmpresa', 'descripcion', 'telefono', 'fotoLogo')

class ProductoForm(forms.ModelForm):
    def clean_foto(self):
        content = self.cleaned_data['foto']
        return validarImagen(content)

    class Meta:
        model = models.Producto
        fields = ('nombre', 'foto', 'tipo', 'certificacion', 'precioUnidad', 'unidadMedida', 'infoAdicional')

class EditarProductoForm(forms.ModelForm):
    def clean_foto(self):
        content = self.cleaned_data['foto']
        return validarImagen(content)

    class Meta:
        model = models.Producto
        fields = ('nombre', 'foto', 'tipo', 'certificacion', 'precioUnidad', 'unidadMedida', 'stock', 'infoAdicional')

class TipoRecogidaForm(forms.ModelForm):
    class Meta:
        model = models.TipoRecogida
        fields = ('direccion', 'diasYHoras')

class GeolocalizacionForm(forms.ModelForm):
    class Meta:
        model = models.Geolocalizacion
        fields = ('latitud', 'longitud')

class FormaCobroForm(forms.ModelForm):
    class Meta:
        model = models.FormaCobro
        fields = ('tipoCobro',)

class ReseñaProductorForm(forms.ModelForm):
    class Meta:
        model = models.ReseñaProductor
        fields = ('calificacion', 'comentario')

class ReseñaProductoForm(forms.ModelForm):
    class Meta:
        model = models.ReseñaProducto
        fields = ('calificacion', 'comentario',)

class MensajeriaForm(forms.ModelForm):
    class Meta:
        model = models.Mensajeria
        fields = ('titulo', 'comentario')

class BlogForm(forms.ModelForm):
    def clean_foto(self):
        content = self.cleaned_data['foto']
        return validarImagen(content)

    class Meta:
        model = models.Blog
        fields = ('titulo', 'articulo', 'foto')

class EditarBlogForm(forms.ModelForm):
    def clean_foto(self):
        content = self.cleaned_data['foto']
        return validarImagen(content)

    class Meta:
        model = models.Blog
        fields = ('titulo', 'articulo', 'foto')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Lo sentimos, esas credenciales son incorrectas. Por favor inténtelo de nuevo.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

def validarImagen(content):
    if isinstance(content, UploadedFile):
        content_type = content.content_type.split('/')[0]
        if content_type in settings.CONTENT_TYPES:
            if content.size > float(settings.MAX_UPLOAD_SIZE):
                raise forms.ValidationError(('El archivo no puede ser mayor a %s. El tamaño es %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        else:
            raise forms.ValidationError(('Formato de archivo incompatible'))
    return content