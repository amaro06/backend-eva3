from django import forms
from .models import Disciplina, Etiqueta, Rutina, Inscripcion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username', 
            'email'
            )
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Correo ya registrado.')
        return email


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

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = [
            'comentario',
            'rutina',
        ]

class PerfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

        self.fields['username'].required = False
        self.fields['email'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            return self.instance.email

        email = email.lower()

        if User.objects.filter(email__iexact=email) \
        .exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo ya está en uso.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username:
            return self.instance.username
        
        return username