from django.contrib import admin
from .models import Profesor, Lugar, Categoria, Taller

# Register your models here.
admin.site.register(Profesor)
admin.site.register(Lugar)
admin.site.register(Categoria)
admin.site.register(Taller)