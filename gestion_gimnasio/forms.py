from django import forms
from .models import Disciplina, Etiqueta, Rutina

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

class RutinaForm(forms.ModelForm):
    class Meta:
        model = Rutina
        fields = [
            'titulo',
            'descripcion',
            'duracion_min',
            'cupos',
            'nivel',
            'disciplina',
            'etiqueta',
        ]