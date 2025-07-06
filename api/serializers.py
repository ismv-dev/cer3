from rest_framework import serializers
from core.models import Taller, Lugar, Categoria, Profesor
import requests
from datetime import date

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class TallerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user

        if not user.is_staff:
            for campo in ['estado', 'observacion']:
                if campo in fields:
                    fields[campo].read_only = True
        return fields
    
    def validate(self, data):
        fecha = data.get('fecha')
        if fecha < date.today():
            data['fecha'] = date.today()
        try:
            response = requests.get('https://api.boostr.cl/holidays.json')
            if response.status_code == 200:
                feriados = response.json()['data']
                irrenunciables = {f['date'] for f in feriados if f['inalienable']==True}
                renunciables = {f['date'] for f in feriados if f['inalienable']==False}
                if fecha.strftime("%Y-%m-%d") in irrenunciables:
                    data['estado'] = 'rechazado'
                    data['observacion'] = 'No se programan talleres en feriados irrenunciables'
                elif fecha.strftime("%Y-%m-%d") in renunciables and data['categoria']!='Aire Libre':
                    data['estado'] = 'rechazado'
        except Exception:
            pass
        return data

class TallerReadSerializer(serializers.ModelSerializer):
    profesor=ProfesorSerializer()
    categoria=CategoriaSerializer()
    lugar=LugarSerializer()
    class Meta:
        model = Taller
        fields = "__all__"