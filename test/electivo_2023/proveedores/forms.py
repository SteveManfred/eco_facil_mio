from django import forms
from .models import Proveedores  
from django.forms import ModelForm




class ProveedoresForm(forms.ModelForm):  

    class Meta:
        model = Proveedores  
        fields = ('nombre','direccion')
        labels = {
            'nombre':'Nombre',
            'direccion':'Direccion'
        }