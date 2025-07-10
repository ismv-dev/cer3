from rest_framework import serializers
from core.models import Taller, Lugar, Categoria, Profesor
from .feriado import dataFeriado
from django import forms
from datetime import date
import logging

logger = logging.getLogger(__name__)

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
        try:
            data = dataFeriado(data)
        except Exception as e:
            logger.error(f"Error in feriado validation: {e}")
            raise serializers.ValidationError(f"Error en validación de fecha: {str(e)}")
        return data

    def validate_titulo(self, value):
        if value:
            value = value.strip()
            if len(value) < 5:
                raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
            if len(value) > 100:
                raise serializers.ValidationError("El título no puede exceder 100 caracteres.")
        return value

    def validate_duracion_horas(self, value):
        if value is not None:
            if value <= 0:
                raise serializers.ValidationError("La duración debe ser mayor a 0 horas.")
            if value > 24:
                raise serializers.ValidationError("La duración no puede exceder 24 horas.")
        return value

    def validate_fecha(self, value):
        if value < date.today():
            raise serializers.ValidationError("La fecha no puede ser anterior a hoy.")
        return value

class TallerReadSerializer(serializers.ModelSerializer):
    profesor = ProfesorSerializer()
    categoria = CategoriaSerializer()
    lugar = LugarSerializer()
    
    class Meta:
        model = Taller
        fields = "__all__"