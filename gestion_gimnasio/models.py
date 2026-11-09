from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Disciplina(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Etiqueta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Rutina(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion_min = models.IntegerField(            #limite de duracion de una rutina
        validators=[                               
            MinValueValidator(10),
            MaxValueValidator(120),
            
        ]
    )
    cupos = models.IntegerField(                   #limite de cupos en una rutina
        validators=[
            
            MinValueValidator(1),
            MaxValueValidator(30),
        ]
    )
    nivel = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT, related_name='rutinas', null=True, blank=True)
    etiqueta = models.ManyToManyField(Etiqueta, related_name='rutinas', blank=True)
    entrenador = models.ForeignKey(User, on_delete=models.PROTECT, related_name='rutinas')

    def __str__(self):
        return self.titulo

class Inscripcion(models.Model):

    estados = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Reachazada'),
    ]

    comentario = models.TextField()
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=estados, default='pendiente')
    socio = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones', null=True, blank=True)
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE, related_name='inscripciones')


