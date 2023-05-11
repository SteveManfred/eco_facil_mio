from django import forms
from .models import Clientes

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ('nombre', 'apellido', 'correo', 'direccion', 'telefono')
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
            'telefono': 'Teléfono'
        }
        
    # Validación de correo electrónico
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if '@' not in correo:
            raise forms.ValidationError('El correo electrónico debe contener un "@"')
        return correo
