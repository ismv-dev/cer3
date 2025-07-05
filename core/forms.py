from django import forms
from .models import Taller, Categoria
import requests

FERIADOS_API_URL = "https://apis.digital.gob.cl/fl/feriados"

def es_feriado(fecha):
    try:
        r = requests.get(FERIADOS_API_URL)
        if r.status_code == 200:
            feriados = {f["fecha"] for f in r.json()}
            return fecha.strftime("%Y-%m-%d") in feriados
    except:
        pass
    return False

class TallerAdminForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = '__all__'

    def clean(self):
        try:
            response = requests.get('https://api.boostr.cl/holidays.json')
            if response.status_code == 200:
                feriados = response.json()['data']
                cleaned_data = super().clean()
                irrenunciables = {f['date'] for f in feriados if f['inalienable']==True}
                renunciables = {f['date'] for f in feriados if f['inalienable']==False}
                if cleaned_data['fecha'].strftime("%Y-%m-%d") in irrenunciables:
                    cleaned_data['estado'] = 'rechazado'
                    cleaned_data['observacion'] = 'No se programan talleres en feriados irrenunciables'
                elif cleaned_data['fecha'].strftime("%Y-%m-%d") in renunciables:
                    cleaned_data['categoria'] = Categoria.objects.get(nombre='Aire Libre')
        except Exception:
            pass
        return cleaned_data
