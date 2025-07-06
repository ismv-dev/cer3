import requests
from datetime import date

def dataFeriado(data):
    if data['fecha'] < date.today():
            data['fecha'] = date.today()
    try:
        response = requests.get("https://apis.digital.gob.cl/fl/feriados")
        if response.status_code == 200:
                feriados = response.json()['data']
                irrenunciables = {f['date'] for f in feriados if f['inalienable']==True}
                renunciables = {f['date'] for f in feriados if f['inalienable']==False}
                if data['fecha'].strftime("%Y-%m-%d") in irrenunciables:
                    data['estado'] = 'rechazado'
                    data['observacion'] = 'No se programan talleres en feriados irrenunciables'
                elif data['fecha'].strftime("%Y-%m-%d") in renunciables and data['categoria']!='Aire Libre':
                    data['estado'] = 'rechazado'
    except Exception:
        pass
    return data