# SchedulesApp

## Descripción del Proyecto

SchedulesApp es un sistema de software web diseñado para automatizar la planificación y gestión de turnos de vigilancia en múltiples edificios. Este sistema aborda los desafíos de asignaciones manuales ineficientes, dificultades en reemplazos por ausencias, inexactitudes en el cálculo de horas trabajadas y la falta de automatización en la generación de reportes.

## Características Principales

- **Enrolamiento de Vigilantes y Edificios:** Permite registrar y gestionar la información de vigilantes y edificios de manera eficiente.
- **Generación Inteligente de Turnos:** Asignación automática de turnos basada en reglas de negocio, optimizando la cobertura de vigilancia.
- **Gestión de Contingencias:** Manejo de ausencias, reemplazos y otras contingencias para asegurar la continuidad del servicio.
- **Cálculo de Horas:** Registro y cálculo automático de horas normales, extras y festivas para una liquidación precisa.
- **Reportes Exportables:** Generación de reportes en formatos PDF y Excel para facilitar el análisis y control.

## Arquitectura

El sistema está construido utilizando una arquitectura **Clean Architecture** combinada con el patrón **MVC**, lo que permite una separación clara de la lógica de negocio, la orquestación de flujos, la infraestructura y la interfaz. Esto facilita la integración con sistemas externos y la realización de pruebas.

## Tecnologías Utilizadas

- **Backend:** Flask, SQLAlchemy, PostgreSQL
- **Frontend:** Next.js 15, Tailwind CSS v4, Radix UI, shadcn/ui
- **Asincronía:** Celery, Redis
- **Autenticación:** JWT, bcrypt
- **Reportes:** Pandas, WeasyPrint, XlsxWriter

## Estructura del Proyecto

```
SchedulesApp/
├── backend/
│   ├── app/
│   │   ├── application/         # Services (business logic)
│   │   ├── domain/             # Models and entities
│   │   ├── infrastructure/     # Database, external APIs
│   │   ├── interface/          # API routes and schemas
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
├── frontend/                   # Next.js 15 App
│   ├── app/                   # App Router pages
│   ├── components/            # React components
│   ├── lib/                   # Utilities and API client
│   ├── package.json
│   └── README.md
├── db/                        # Database scripts
├── docker-compose.yml
└── README.md
```

## Instalación y Desarrollo

### Requisitos Previos

- **Node.js** 18+ y npm
- **Python** 3.9+
- **PostgreSQL** 13+
- **Redis** 6+ (opcional, para funciones avanzadas)
- **Docker** y Docker Compose (para ejecución con contenedores)

### Configuración Rápida con Docker (Recomendado)

1. **Clone el repositorio**
```bash
git clone <URL del repositorio>
cd SchedulesApp
```

2. **Configure las variables de entorno**
```bash
# Copie los archivos de ejemplo
cp .env.example .env
cp frontend/.env.example frontend/.env.local

# Edite los archivos .env según su entorno
```

3. **Inicie todos los servicios**
```bash
docker-compose up --build
```

4. **Configure la base de datos y usuario demo**
```bash
# En otra terminal, ejecute las migraciones
docker-compose exec backend python -c "from app.infrastructure.database import create_tables; create_tables()"

# Cree un usuario demo para pruebas
docker-compose exec backend python create_demo_user.py
```

5. **Acceda a la aplicación**
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000/api
- **Documentación API:** http://localhost:5000/api/docs (si está configurado)

### Desarrollo Local Manual

#### Backend

1. **Configure el entorno Python**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Instale dependencias**
```bash
pip install -r requirements.txt
```

3. **Configure la base de datos**
```bash
# Asegúrese de que PostgreSQL esté ejecutándose
# Cree la base de datos
createdb schedules_db

# Configure las variables de entorno
cp ../.env.example .env
# Edite .env con su configuración de base de datos
```

4. **Ejecute el backend**
```bash
python app/main.py
```

#### Frontend

1. **Configure el entorno Node.js**
```bash
cd frontend
npm install
```

2. **Configure las variables de entorno**
```bash
cp .env.example .env.local
# Edite .env.local si es necesario
```

3. **Ejecute el frontend**
```bash
npm run dev
```

### Credentials de Prueba

Después de ejecutar `create_demo_user.py`:
- **Username:** admin
- **Password:** admin123
- **Role:** operator

### Comandos Útiles

```bash
# Verificar estado de servicios (Docker)
docker-compose ps

# Ver logs del backend
docker-compose logs backend

# Ver logs del frontend
docker-compose logs frontend

# Reiniciar solo un servicio
docker-compose restart backend

# Ejecutar migraciones
docker-compose exec backend python -c "from app.infrastructure.database import create_tables; create_tables()"

# Acceder a la base de datos
docker-compose exec db psql -U user -d schedules_db

# Limpiar y reconstruir
docker-compose down -v
docker-compose up --build
```

### Estructura de Archivos de Configuración

```
SchedulesApp/
├── .env                     # Variables de entorno del backend
├── .env.example            # Plantilla de variables de entorno
├── docker-compose.yml      # Configuración de Docker
├── backend/
│   ├── requirements.txt    # Dependencias Python
│   ├── create_demo_user.py # Script para crear usuario demo
│   └── app/
│       ├── config.py       # Configuración de la aplicación
│       └── ...
└── frontend/
    ├── .env.local          # Variables de entorno del frontend
    ├── .env.example        # Plantilla de variables de entorno
    ├── package.json        # Dependencias Node.js
    └── ...
```

### Solución de Problemas

**Error de conexión a la base de datos:**
- Verifique que PostgreSQL esté ejecutándose
- Verifique las credenciales en `.env`
- Asegúrese de que la base de datos existe

**Error de autenticación JWT:**
- Verifique que `JWT_SECRET_KEY` esté configurado en `.env`
- Verifique que el frontend esté usando la URL correcta de la API

**Errores de CORS:**
- Asegúrese de que el backend permita el origen del frontend
- Verifique la configuración en `app/config.py`

### Base de Datos

La aplicación usa PostgreSQL con las siguientes tablas principales:
- `vigilantes` - Información de vigilantes
- `buildings` - Información de edificios
- `shifts` - Turnos asignados
- `users` - Usuarios del sistema
- `reports` - Reportes generados

## Contribuciones

Las contribuciones son bienvenidas. Si desea contribuir, por favor abra un issue o envíe un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulte el archivo LICENSE para más detalles.