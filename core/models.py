from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Profesor(models.Model):
    nombre_completo = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_completo

class Lugar(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre

class Taller(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateField()
    duracion_horas = models.FloatField(validators=[MinValueValidator(0)])
    estado = models.CharField(max_length=20, choices=(('pendiente', 'pendiente'),('aceptado', 'aceptado'),('rechazado', 'rechazado')), default='pendiente')
    profesor = models.ForeignKey(Profesor, null=True, blank=True, on_delete=models.CASCADE)
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    observacion = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.titulo