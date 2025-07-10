from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Categoria, Taller
from django.views.decorators.csrf import csrf_protect
from datetime import date
from django.contrib import messages
from .forms import LoginForm, TallerForm
from django.core.exceptions import ValidationError
from django.http import Http404
import logging

logger = logging.getLogger(__name__)

def home_view(request):
    try:
        # datos base
        '''
        l1 = [(1, 'Aire Libre', 'Actividades que se realizan al exterior, como yoga, caminatas o deporte.'),
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
        talleres = Taller.objects.filter(estado='aceptado', fecha__gte=date.today()).order_by('fecha')
        
        # Sanitize and validate category filter
        categoria = request.GET.get('categoria')
        if categoria:
            try:
                categoria_id = int(categoria)
                talleres = talleres.filter(categoria_id=categoria_id)
            except (ValueError, TypeError):
                # Invalid category ID, ignore filter
                pass
        
        data = {
            'categorias': categorias,
            'talleres': talleres,
        }
        return render(request, 'core/index.html', data)
    except Exception as e:
        logger.error(f"Error in home_view: {e}")
        messages.error(request, "Error al cargar la página. Por favor, inténtelo de nuevo.")
        return render(request, 'core/index.html', {'categorias': [], 'talleres': []})

@login_required
def newTaller_view(request):
    try:
        form = TallerForm(request.POST or None, request=request)
        if request.method == 'POST':
            if form.is_valid():
                taller = form.save(commit=False)
                # Set default values for non-staff users
                if not request.user.is_staff:
                    taller.estado = 'pendiente'
                    taller.observacion = ''
                taller.save()
                messages.success(request, "Taller creado exitosamente.")
                return redirect('home')
            else:
                messages.error(request, "Por favor, corrija los errores en el formulario.")
        
        return render(request, 'core/newTaller.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in newTaller_view: {e}")
        messages.error(request, "Error al crear el taller. Por favor, inténtelo de nuevo.")
        return redirect('home')

@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    try:
        form = LoginForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    request.session.set_expiry(7200)  # 2 hours
                    messages.success(request, f"Bienvenido, {user.username}!")
                    return redirect('home')
                else:
                    messages.error(request, "Su cuenta está deshabilitada.")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
                logger.warning(f"Failed login attempt for username: {username}")
        
        return render(request, 'core/login.html', {'form': form})
    except Exception as e:
        logger.error(f"Error in login_view: {e}")
        messages.error(request, "Error en el sistema de autenticación. Por favor, inténtelo de nuevo.")
        return render(request, 'core/login.html', {'form': LoginForm()})

def logout_view(request):
    try:
        logout(request)
        messages.success(request, "Sesión cerrada exitosamente.")
    except Exception as e:
        logger.error(f"Error in logout_view: {e}")
    return redirect('home')
