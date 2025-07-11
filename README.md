# Municipalidad Villa Verde - Sistema de Talleres

Sistema web para la gestión de talleres municipales con funcionalidades de administración y API REST.

## Características

- ✅ Gestión de talleres municipales
- ✅ Sistema de autenticación seguro
- ✅ API REST con DRF
- ✅ Validación de fechas y feriados
- ✅ Interfaz web responsive
- ✅ Sistema de permisos por roles

## Instalación

### Requisitos

- Python 3.8+
- Django 5.2+
- SQLite (desarrollo) / PostgreSQL (producción)

### Configuración

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd municipalidad2
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env basado en .env.example
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones**
```bash
python manage.py migrate
```

6. **Crear superusuario**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor**
```bash
python manage.py runserver
```

## Configuración de Seguridad

### Variables de Entorno Requeridas

```bash
# Configuración básica
DEBUG=False
SECRET_KEY=tu-clave-secreta-muy-segura
ALLOWED_HOSTS=localhost,127.0.0.1,tudominio.com

# Configuración de seguridad
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Verificación de Seguridad

Ejecuta el comando de verificación de seguridad:

```bash
python manage.py security_check
```

### Configuración para Producción

1. **Configurar HTTPS**
   - Obtener certificado SSL
   - Configurar proxy reverso (nginx/apache)
   - Habilitar redirección HTTPS

2. **Base de datos**
   - Usar PostgreSQL en lugar de SQLite
   - Configurar backups automáticos
   - Usar conexiones SSL

3. **Servidor web**
   - Configurar nginx/apache
   - Habilitar compresión gzip
   - Configurar cache de archivos estáticos

## Estructura del Proyecto

```
municipalidad2/
├── api/                    # API REST
│   ├── feriado.py         # Validación de feriados
│   ├── serializers.py     # Serializers DRF
│   ├── urls.py           # URLs de la API
│   └── views.py          # Viewsets DRF
├── core/                  # Aplicación principal
│   ├── forms.py          # Formularios
│   ├── middleware.py     # Middleware de seguridad
│   ├── models.py         # Modelos de datos
│   ├── templates/        # Templates HTML
│   ├── static/          # Archivos estáticos
│   └── views.py         # Vistas web
├── municipalidad/        # Configuración del proyecto
│   ├── settings.py      # Configuración Django
│   └── urls.py          # URLs principales
└── requirements.txt     # Dependencias
```

## API REST

### Endpoints

- `GET /api/Talleres/` - Listar talleres
- `POST /api/Talleres/` - Crear taller
- `GET /api/Talleres/{id}/` - Obtener taller
- `PUT /api/Talleres/{id}/` - Actualizar taller
- `DELETE /api/Talleres/{id}/` - Eliminar taller
- `POST /api/Talleres/{id}/approve/` - Aprobar taller (admin)
- `POST /api/Talleres/{id}/reject/` - Rechazar taller (admin)

### Autenticación

La API requiere autenticación por sesión o básica HTTP.

### Ejemplo de uso

```bash
# Listar talleres
curl -H "Authorization: Basic <credentials>" http://localhost:8000/api/Talleres/

# Crear taller
curl -X POST -H "Content-Type: application/json" \
     -H "X-CSRFToken: <token>" \
     -d '{"titulo":"Taller de Yoga","fecha":"2024-01-15"}' \
     http://localhost:8000/api/Talleres/
```

## Modelos de Datos

### Taller
- `titulo`: Título del taller
- `fecha`: Fecha del taller
- `duracion_horas`: Duración en horas
- `estado`: pendiente/aceptado/rechazado
- `profesor`: Profesor asignado
- `lugar`: Lugar del taller
- `categoria`: Categoría del taller
- `observacion`: Observaciones

### Profesor
- `nombre_completo`: Nombre completo del profesor

### Lugar
- `nombre`: Nombre del lugar

### Categoria
- `nombre`: Nombre de la categoría

## Funcionalidades de Seguridad

### ✅ Implementadas

- **Autenticación segura**: Login con validación de credenciales
- **CSRF Protection**: Protección contra ataques CSRF
- **Rate Limiting**: Limitación de intentos de login
- **Input Validation**: Validación de entrada de datos
- **SQL Injection Protection**: ORM de Django
- **XSS Protection**: Headers de seguridad
- **Content Security Policy**: CSP headers
- **Session Security**: Cookies seguras y expiración
- **Password Validation**: Validación de contraseñas
- **Error Handling**: Manejo seguro de errores
- **Logging**: Registro de eventos de seguridad

### 🔒 Configuraciones de Seguridad

- **SECRET_KEY**: Generación automática segura
- **DEBUG**: Configurable por entorno
- **ALLOWED_HOSTS**: Validación de hosts
- **HTTPS**: Redirección SSL configurable
- **HSTS**: HTTP Strict Transport Security
- **Secure Cookies**: Cookies solo HTTPS
- **Session Timeout**: Expiración de sesiones
- **Password Hashers**: Argon2, PBKDF2, BCrypt

## Comandos Útiles

```bash
# Verificar configuración de seguridad
python manage.py security_check

# Verificar configuración de producción
python manage.py check --deploy

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic
```

## Desarrollo

### Estructura de Desarrollo

1. **Feature Branches**: Usar ramas para nuevas funcionalidades
2. **Code Review**: Revisión obligatoria de código
3. **Testing**: Escribir tests para nuevas funcionalidades
4. **Documentation**: Documentar cambios importantes

### Testing

```bash
# Ejecutar tests
python manage.py test

# Ejecutar tests con coverage
coverage run --source='.' manage.py test
coverage report
```

## Despliegue

### Checklist de Producción

- DEBUG=False
- SECRET_KEY configurado
- ALLOWED_HOSTS configurado
- HTTPS habilitado
- Base de datos configurada
- Archivos estáticos recolectados
- Logs configurados
- Backups configurados
- Monitoreo configurado

### Servicios Recomendados

- **Web Server**: nginx
- **Application Server**: gunicorn
- **Database**: PostgreSQL
- **Cache**: Redis
- **Monitoring**: Sentry
- **Backup**: Automatizado
