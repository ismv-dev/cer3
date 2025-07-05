from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as lgout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Categoria, Lugar, Taller
from datetime import date
from django.contrib import messages
import requests
try:
    response=requests.get('https://api.boostr.cl/holidays.json')
    response.raise_for_status()
    feriados = response.json()['data']
except requests.exceptions.RequestException as e:
        datos = {'error': str(e)}



def home(request):
    '''l1 = [(1, 'Aire Libre', 'Actividades que se realizan al exterior, como yoga, caminatas o deporte.'),
(2, 'Arte', 'Talleres de pintura, dibujo, manualidades, escultura, mosaico, etc.'),
(3, 'Música', 'Talleres de guitarra, canto, instrumentos, folclore o ensamble.'),
(4, 'Salud', 'Actividades relacionadas con bienestar físico o mental: meditación, autocuidado, etc.'),
(5, 'Tecnología', 'Capacitación en herramientas digitales, alfabetización digital, computación básica.'),
(6, 'Oficios', 'Actividades orientadas al emprendimiento: costura, panadería, carpintería, etc.'),
(7, 'Educación', 'Apoyo escolar, alfabetización, talleres de idiomas, matemáticas, etc.'),
(8, 'Medioambiente', 'Huertos urbanos, reciclaje, compostaje, educación ambiental.'),
(9, 'Comunidad y Liderazgo', 'Formación ciudadana, liderazgo, gestión vecinal, resolución de conflictos.'),
(10, 'Recreación', 'Juegos, dinámicas grupales, talleres lúdicos para todas las edades.')]

    l2 = [(1, 'Jardín Botánico', 'Av. del Parque 123, Villa Verde'),
    (2, 'Playa El Encanto', 'Costanera Sur s/n, Sector Costero'),
    (3, 'Biblioteca Municipal', 'Calle Los Libros 45, Centro Cívico'),
    (4, 'Centro Cultural Villa Verde', 'Av. Patrimonio 567, Barrio Histórico'),
    (5, 'Gimnasio Municipal', 'Av. Deportes 789, Villa Deportiva'),
    (6, 'Sede Junta Vecinal N°5', 'Pasaje Los Almendros 321, Sector Norte'),
    (7, 'Sede Junta Vecinal N°12', 'Calle La Esperanza 876, Sector Sur'),
    (8, 'Parque Comunal', 'Camino Verde km 2, Acceso Norte'),
    (9, 'Salón Multiuso Municipal', 'Edificio Consistorial, 2° piso'),
    (10, 'Escuela Básica Villa Verde', 'Calle Educación 234, Sector Escolar')]'''
    for a in l1:
        categoria = Categoria()
        categoria.nombre = a[1]
        categoria.save()
    for a in l2:
        lugar = Lugar()
        lugar.nombre = a[1]
        lugar.save()
    talleres = list(Taller.objects.filter(fecha__month=date.today().month, estado='aceptado'))
    data = {
        'talleres': talleres,
    }
    return render(request, 'core/index.html', data)

def registro(request):
    if request.POST:
        if request.POST['email']=='' or request.POST['nombre']=='' or request.POST['password']=='':
            messages.error(request, 'Ningún campo obligatorio puede estar vacío')
        elif User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, 'Correo ya registrado')
        elif request.POST['password']==request.POST['confirmPassword']:
            user = User.objects.create_user(username=request.POST['email'], first_name=request.POST['nombre'], last_name=request.POST['apellido'], email=request.POST['email'], password=request.POST['password'])
            login(request, user)
            messages.success(request, 'Cuenta creada correctamente')
            return redirect('home')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
    return render(request, 'core/registro.html')

def ingresar(request):
    if request.POST:
        usuario = authenticate(username=request.POST['email'], password=request.POST['password'])
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorrecta')
    return render(request, 'core/ingresar.html')

def logout(request):
    lgout(request)
    return redirect('home')