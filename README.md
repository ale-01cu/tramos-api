# Tramos API

Tramos API es un sistema RESTful robusto y escalable desarrollado con Django y Django REST Framework. Proporciona una solución integral para la gestión de cursos, ofertas académicas, inscripciones, clientes y pagos, orientado a instituciones educativas.

## ✨ Características Principales

- **Gestión de Usuarios y Roles:** Sistema de autenticación basado en JWT con múltiples roles (admin, gestor, comercial, cajero, observador) para un control de acceso granular.
- **Gestión Académica Completa:** Administración de Servicios, Cursos, Escuelas, Aulas y Ofertas de cursos.
- **Sistema de Reservas:** Manejo de reservas para clientes individuales y reservas múltiples para empresas.
- **Gestión de Clientes y Empresas:** Registro y seguimiento de información de clientes y convenios con empresas.
- **Integración de Pagos:** Pasarela de pago implementada con Transfermóvil para procesar los pagos de las reservas.
- **Generación de Reportes:** Endpoints dedicados para generar reportes dinámicos como listas de asistencia, hojas de registro y reportes de comparecencia.
- **Documentación de API Automatizada:** Documentación interactiva y detallada de la API disponible a través de Swagger UI y Redoc.
- **Trazabilidad de Acciones:** Middleware para registrar las acciones importantes que ocurren en el sistema.

## 🛠️ Tecnologías Utilizadas

- **Backend:** Python, Django
- **API:** Django REST Framework
- **Base de Datos:** PostgreSQL (a través de `psycopg2`)
- **Autenticación:** JSON Web Tokens (JWT) con `djangorestframework-simplejwt`
- **Documentación de API:** `drf-spectacular` para generar esquemas OpenAPI (Swagger/Redoc).
- **Variables de Entorno:** `django-environ`
- **Servidor de Producción:** Gunicorn
- **Otros:** `requests` para comunicación con servicios externos.

## 📂 Estructura del Proyecto

```
tramos-api/
├── api/                    # Directorio principal de la aplicación de la API
│   ├── migrations/         # Migraciones de la base de datos
│   ├── models/             # Modelos de Django (esquema de la BD)
│   ├── middleware/         # Middlewares personalizados
│   ├── v1/                 # Versión 1 de la API
│   │   ├── filters/        # Clases de filtros para los viewsets
│   │   ├── permissions/    # Permisos personalizados
│   │   ├── serializers/    # Serializadores para los modelos
│   │   ├── viewsets/       # Lógica de los endpoints (Vistas)
│   │   └── urls.py         # Rutas de la API v1
│   └── ...
├── tramos_api/             # Configuración del proyecto Django
│   ├── settings.py         # Configuración principal
│   └── urls.py             # Rutas principales del proyecto
├── .env                    # Archivo para variables de entorno (no versionado)
├── manage.py               # Utilidad de línea de comandos de Django
└── requirements.txt        # Dependencias de Python
```

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para configurar el entorno de desarrollo local.

**1. Clonar el Repositorio**
```bash
git clone <URL_DEL_REPOSITORIO>
cd tramos-api
```

**2. Crear y Activar un Entorno Virtual**
```bash
# En Windows
python -m venv .venv
.venv\Scripts\activate

# En macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

**4. Configurar Variables de Entorno**
Crea un archivo llamado `.env` en la raíz del proyecto y añade las siguientes variables. Reemplaza los valores con tu configuración.

```ini
# Tramos API .env file
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='tu_clave_secreta_aqui'

# DEBUG: True para desarrollo, False para producción
DEBUG=True

# Configuración de la Base de Datos (ejemplo para PostgreSQL)
DATABASE_URL='psql://usuario:contraseña@localhost:5432/nombre_db'

# Configuración de Transfermóvil
TM_USERNAME='tu_usuario_tm'
TM_SEED='tu_semilla_tm'
TM_SOURCE='tu_source_tm'
TM_CURRENCY='CUP'
TM_URL_RESPONSE_TRANSFERMOVIL='https://tu-dominio.com/api/v1/payment/notification/'
TM_CONNECTION='https://api-transfermovil.com/api' # URL de la API de Transfermóvil
```

**5. Ejecutar Migraciones**
Aplica las migraciones para crear el esquema de la base de datos.
```bash
python manage.py migrate
```

**6. Crear un Superusuario**
Esto te permitirá acceder al panel de administración de Django.
```bash
python manage.py createsuperuser
```

**7. Ejecutar el Servidor de Desarrollo**
```bash
python manage.py runserver
```
El API estará disponible en `http://127.0.0.1:8000/`.

## 📚 Endpoints de la API

La API está versionada y todos los endpoints principales se encuentran bajo el prefijo `/api/v1/`.

### Autenticación
- `POST /api/token/`: Obtiene un par de tokens (acceso y refresco) a partir de credenciales de usuario.
- `POST /api/token/refresh/`: Refresca un token de acceso expirado.

### Gestión Principal
- `/user/`: Gestión de usuarios (CRUD).
- `/province/`, `/municipality/`: Gestión de provincias y municipios.
- `/school/`, `/classroom/`: Gestión de escuelas y aulas.
- `/service/`, `/course/`: Gestión de servicios y cursos.
- `/offer/`: Gestión de ofertas de cursos.
- `/client/`: Gestión de clientes.
- `/company/`: Gestión de empresas.
- `/booking/`: Gestión de reservas individuales.
- `/multipleBooking/`: Gestión de reservas para empresas.
- `/payment-code/`: Gestión de códigos de pago.

### Pagos y Reportes
- `POST /api/v1/payment/register/`: Inicia un proceso de pago con Transfermóvil.
- `POST /api/v1/payment/notification/`: Endpoint para recibir notificaciones de pago de Transfermóvil.
- `GET /api/v1/reports/offer/current`: Lista las ofertas actuales.
- `GET /api/v1/reports/course-evaluation/`: Genera reportes detallados de cursos.

## 🧪 Ejecución de Pruebas

Para ejecutar el conjunto de pruebas y verificar la integridad del código, utiliza el siguiente comando:
```bash
python manage.py test api
```

## 📄 Documentación Interactiva

Este proyecto utiliza `drf-spectacular` para generar una documentación de API interactiva. Una vez que el servidor esté en funcionamiento, puedes acceder a:

- **Swagger UI:** `http://127.0.0.1:8000/api/v1/swagger/`
- **Redoc:** `http://127.0.0.1:8000/api/v1/redoc/`

Estas interfaces te permitirán explorar todos los endpoints, ver los parámetros que aceptan y probarlos en tiempo real.