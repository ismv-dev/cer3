from django import forms
from .models import Taller, Categoria
from api.feriado import dataFeriado

FERIADOS_API_URL = "https://apis.digital.gob.cl/fl/feriados"

class TallerAdminForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = '__all__'

    def clean(self):
        data = super().clean()
        data = dataFeriado(data)
        return data
