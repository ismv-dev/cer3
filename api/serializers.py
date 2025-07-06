from rest_framework import serializers
from core.models import Taller, Lugar, Categoria, Profesor
from .feriado import dataFeriado

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
        data=dataFeriado(data)
        return data

class TallerReadSerializer(serializers.ModelSerializer):
    profesor=ProfesorSerializer()
    categoria=CategoriaSerializer()
    lugar=LugarSerializer()
    class Meta:
        model = Taller
        fields = "__all__"