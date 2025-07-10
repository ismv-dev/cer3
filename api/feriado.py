import requests
from datetime import date
from rest_framework import serializers
from core.models import Lugar, Categoria

def dataFeriado(data):
    if data['fecha'] < date.today():
        raise serializers.ValidationError("La fecha no puede ser anterior a hoy.")

    try:
        response = requests.get("https://api.boostr.cl/holidays.json", timeout=10)
        response.raise_for_status()

        feriados = response.json().get('data', [])
        fecha_str = data['fecha'].strftime("%Y-%m-%d")

        irrenunciables = {f['date'] for f in feriados if f.get('inalienable') is True}
        renunciables = {f['date'] for f in feriados if f.get('inalienable') is False}

        if fecha_str in irrenunciables:
            data['estado'] = 'rechazado'
            data['observacion'] = 'No se programan talleres en feriados irrenunciables'
        elif fecha_str in renunciables:
            # Check if the category is "Aire Libre" by getting the category name
            categoria = data.get('categoria')
            if hasattr(categoria, 'nombre'):
                categoria_nombre = categoria.nombre
            else:
                # If it's an ID, get the category name
                try:
                    categoria_obj = Categoria.objects.get(id=categoria)
                    categoria_nombre = categoria_obj.nombre
                except:
                    categoria_nombre = ""
            
            if categoria_nombre != 'Aire Libre':
                data['estado'] = 'rechazado'
                data['observacion'] = 'Sólo se programan talleres al aire libre en feriados'

    except requests.RequestException as e:
        # Log the error but don't fail the validation
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error consultando feriados: {e}")
    except (ValueError, KeyError) as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Error procesando datos de feriados: {e}")

    return data
