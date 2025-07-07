from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as lgout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Categoria, Lugar, Taller
from datetime import date
from django.contrib import messages

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
    (10, 'Escuela Básica Villa Verde', 'Calle Educación 234, Sector Escolar')]
    for a in l1:
        categoria = Categoria()
        categoria.nombre = a[1]
        categoria.save()
    for a in l2:
        lugar = Lugar()
        lugar.nombre = a[1]
        lugar.save()'''
    
    categorias = Categoria.objects.all()
    talleres = Taller.objects.filter(estado='aceptado', fecha__gte=date.today())
    categoria = request.GET.get('categoria')
    if categoria:
        talleres = talleres.filter(categoria=categoria)
    data = {
        'categorias': categorias,
        'talleres': talleres,
    }
    return render(request, 'core/index.html', data)

def ingresar(request):
    if request.POST:
        usuario = authenticate(username=request.POST['username'], password=request.POST['password'])
        if usuario is not None:
            login(request, usuario)
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorrecta')
    return render(request, 'core/ingresar.html')

def logout(request):
    lgout(request)
    return redirect('home')
