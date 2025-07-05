from django.contrib import admin
from .models import Profesor, Lugar, Categoria, Taller
from .forms import TallerAdminForm

# Register your models here.
admin.site.register(Profesor)
admin.site.register(Lugar)
admin.site.register(Categoria)
@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    form = TallerAdminForm