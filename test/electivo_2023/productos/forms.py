from django import forms
from .models import Producto  
from django.forms import ModelForm




class ProductosForm(forms.ModelForm): 

    class Meta:
        model = Producto  
        fields = ('nombre','material','cantidad','categoria')
        labels = {
            'nombre':'Nombre',
            'cantidad':'n. cantidad'
        }

    def __init__(self, *args, **kwargs):
        super(ProductosForm,self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Select"
        self.fields['cantidad'].required = False