from django import forms
from .models import Disciplina, Etiqueta

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = [
            'nombre',
        ]

class EtiquetaForm(forms.ModelForm):
    class Meta:
        model = Etiqueta
        fields = [
            'nombre',
        ]