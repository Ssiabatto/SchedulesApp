# SchedulesApp - Sistema de Gestión de Turnos para Vigilantes

## 📋 Descripción

SchedulesApp es un sistema web para automatizar la planificación y gestión de turnos de vigilancia en múltiples edificios. Soluciona problemas de asignaciones manuales ineficientes, dificultades en reemplazos por ausencias, inexactitudes en el cálculo de horas trabajadas y la falta de automatización en la generación de reportes.

## ✨ Características Principales

- **Gestión de Vigilantes**: Registro completo con datos personales, certificaciones y habilidades
- **Gestión de Edificios**: Administración de propiedades y requerimientos de seguridad
- **Planificación Inteligente**: Asignación automática de turnos basada en reglas de negocio
- **Gestión de Contingencias**: Manejo de ausencias, reemplazos y emergencias
- **Cálculo de Horas**: Registro automático de horas normales, extras y festivas
- **Reportes Exportables**: Generación de reportes en PDF y Excel
- **Autenticación Segura**: Sistema JWT con roles de usuario
- **Dashboard Interactivo**: Interfaz moderna y responsiva

## 🏗️ Arquitectura Técnica

### Backend - Clean Architecture
- **Domain Layer**: Modelos de negocio y reglas empresariales
- **Application Layer**: Servicios y casos de uso
- **Infrastructure Layer**: Base de datos PostgreSQL y APIs externas
- **Interface Layer**: API REST con Flask

### Frontend - Arquitectura Moderna
- **Framework**: Next.js 15 con App Router
- **UI/UX**: Tailwind CSS + shadcn/ui components
- **Estado**: React hooks y Context API
- **API Client**: TypeScript con manejo de errores

### Base de Datos
- **PostgreSQL 13+**: Base de datos principal con 15 tablas
- **Schema**: `PostgreDB.sql` con triggers, funciones y constraints
- **ORM**: SQLAlchemy con patrón Repository

## 🛠️ Stack Tecnológico

| Categoría | Tecnología | Versión | Propósito |
|-----------|------------|---------|-----------|
| **Backend** | Python | 3.11+ | API y lógica de negocio |
| **Framework** | Flask | 2.3+ | Web framework |
| **ORM** | SQLAlchemy | 2.0+ | Object-Relational Mapping |
| **Base de Datos** | PostgreSQL | 13+ | Almacenamiento principal |
| **Autenticación** | Flask-JWT-Extended | 4.5+ | Tokens JWT |
| **Seguridad** | bcrypt | 4.0+ | Hash de contraseñas |
| **Frontend** | Next.js | 15+ | React framework |
| **Estilos** | Tailwind CSS | 4+ | Utility-first CSS |
| **Componentes** | shadcn/ui | Latest | Component library |
| **Contenedores** | Docker | 24+ | Contenerización |
| **Orquestación** | Docker Compose | 2.20+ | Multi-container |
| **Cache** | Redis | 7+ | Cache y sessions |

## 📊 Estructura del Proyecto

```
SchedulesApp/
├── 📁 backend/                    # API Python Flask
│   ├── 📁 app/
│   │   ├── 📁 domain/             # Entidades y reglas de negocio
│   │   │   ├── models.py          # Modelos de dominio
│   │   │   ├── repositories.py    # Interfaces de repositorio
│   │   │   └── services.py        # Servicios de dominio
│   │   ├── 📁 application/        # Casos de uso y servicios
│   │   │   └── services.py        # Orquestación de flujos
│   │   ├── 📁 infrastructure/     # Base de datos y APIs externas
│   │   │   ├── database.py        # SQLAlchemy models y repos
│   │   │   ├── celery_worker.py   # Tareas asíncronas
│   │   │   └── odoo_api.py        # Integración Odoo
│   │   ├── 📁 interface/          # API REST y schemas
│   │   │   ├── 📁 api/
│   │   │   │   └── auth.py        # Endpoints de autenticación
│   │   │   └── schemas.py         # Pydantic schemas
│   │   ├── config.py              # Configuración de la app
│   │   └── main.py                # Punto de entrada
│   ├── create_demo_user.py        # Script usuario demo
│   ├── init_db.py                 # Inicialización BD
│   ├── requirements.txt           # Dependencias Python
│   └── Dockerfile                 # Container backend
├── 📁 frontend/                   # App Next.js React
│   ├── 📁 app/                    # App Router pages
│   │   ├── layout.tsx             # Layout principal
│   │   ├── page.tsx               # Homepage
│   │   ├── 📁 dashboard/          # Dashboard principal
│   │   ├── 📁 guards/             # Gestión vigilantes
│   │   ├── 📁 buildings/          # Gestión edificios
│   │   ├── 📁 contracts/          # Gestión contratos
│   │   └── 📁 reports/            # Reportes y analytics
│   ├── 📁 components/             # Componentes React
│   │   ├── 📁 ui/                 # Componentes shadcn/ui
│   │   ├── guards-table.tsx       # Tabla de vigilantes
│   │   ├── buildings-table.tsx    # Tabla de edificios
│   │   └── calendar-view.tsx      # Vista de calendario
│   ├── 📁 lib/                    # Utilidades y API
│   │   ├── api.ts                 # Cliente API
│   │   └── utils.ts               # Funciones utilitarias
│   ├── package.json               # Dependencias Node.js
│   └── Dockerfile                 # Container frontend
├── 📁 db/                         # Scripts de base de datos
│   ├── PostgreDB.sql              # Schema principal PostgreSQL
│   └── MariaDB.sql                # Schema alternativo MariaDB
├── docker-compose.yml             # Orquestación servicios
├── .env.example                   # Variables de entorno ejemplo
├── .gitignore                     # Archivos ignorados por Git
├── swagger.yaml                   # Documentación API
├── test_integration.py            # Tests de integración
├── README.md                      # Este archivo
└── LICENSE                        # Licencia MIT
```

## 🚀 Instalación y Configuración

### Opción 1: Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd SchedulesApp
```

2. **Configurar variables de entorno**
```bash
cp .env.example .env
cp frontend/.env.example frontend/.env.local
# Editar archivos .env según necesidades
```

3. **Levantar servicios**
```bash
docker-compose up --build -d
```

4. **Inicializar base de datos**
```bash
docker-compose exec backend python init_db.py
docker-compose exec backend python create_demo_user.py
```

5. **Verificar instalación**
```bash
python test_integration.py
```

### Opción 2: Desarrollo Local

#### Backend Setup

1. **Crear entorno virtual**
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**
```bash
# Instalar PostgreSQL
# Crear base de datos: gestion_turnos_vigilantes
# Configurar variables en .env
```

4. **Ejecutar backend**
```bash
python init_db.py  # Primera vez
python app/main.py
```

#### Frontend Setup

1. **Instalar dependencias**
```bash
cd frontend
npm install
```

2. **Configurar variables**
```bash
cp .env.example .env.local
# Configurar NEXT_PUBLIC_API_URL
```

3. **Ejecutar frontend**
```bash
npm run dev
```

## 🔧 Configuración

### Variables de Entorno

**Backend (.env)**
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/gestion_turnos_vigilantes
SECRET_KEY=your_super_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
CELERY_BROKER_URL=redis://localhost:6379/0
FLASK_ENV=development
```

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### Base de Datos

La aplicación utiliza PostgreSQL con el schema definido en `db/PostgreDB.sql`:

- **15 Tablas principales**: usuarios, vigilantes, edificios, turnos, etc.
- **Triggers y Funciones**: Validaciones automáticas y cálculos
- **Constraints**: Integridad referencial y reglas de negocio
- **Índices**: Optimización para consultas frecuentes

## 📚 API Documentation

La documentación completa de la API está disponible en `swagger.yaml`. Principales endpoints:

### Autenticación
- `POST /api/auth/login` - Login de usuario
- `POST /api/auth/register` - Registro de usuario
- `GET /api/auth/protected` - Endpoint protegido de prueba

### Gestión de Vigilantes
- `GET /api/vigilantes` - Listar vigilantes
- `POST /api/vigilantes` - Crear vigilante
- `GET /api/vigilantes/{id}` - Obtener vigilante
- `PUT /api/vigilantes/{id}` - Actualizar vigilante
- `DELETE /api/vigilantes/{id}` - Eliminar vigilante

### Gestión de Edificios
- `GET /api/buildings` - Listar edificios
- `POST /api/buildings` - Crear edificio
- Similar CRUD para edificios

### Gestión de Turnos
- `GET /api/shifts` - Listar turnos
- `POST /api/shifts` - Crear turno
- Filtros por vigilante, edificio, fecha

## 🧪 Testing

### Tests de Integración
```bash
# Con Docker ejecutándose
python test_integration.py
```

### Tests Manuales
1. Acceder a http://localhost:3000
2. Login con credenciales demo: `admin` / `admin123`
3. Navegar por los módulos del dashboard
4. Probar creación de vigilantes y edificios

### Verificación de Endpoints
```bash
# Health check
curl http://localhost:5000/api/health

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Para instrucciones detalladas de testing, consultar: [TESTING_GUIDE.md](TESTING_GUIDE.md)**

## 📋 Historial de Versiones

El desarrollo completo del proyecto está documentado en [CHANGELOG.md](CHANGELOG.md), donde se puede consultar:

- **v1.0.0** (2025-07-09): Versión de producción con documentación completa, testing y seguridad
- **v0.9.0** (2025-06-20): Beta con PostgreSQL, Clean Architecture y UI completa
- **v0.8.0** (2025-05-25): Alpha con fundamentos backend y frontend básico
- **Versiones anteriores**: Planificación, diseño y análisis de requisitos

Ver [CHANGELOG.md](CHANGELOG.md) para detalles completos de cada versión.

## 👤 Credenciales Demo

**Usuario Administrador:**
- Username: `admin`
- Password: `admin123`
- Role: `operador_supervisor`

## 🔐 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Hash de Contraseñas**: bcrypt con salt
- **Validación de Entrada**: Sanitización en backend y frontend
- **CORS**: Configurado para dominios permitidos
- **Variables de Entorno**: Credenciales y secrets seguros

## 📈 Monitoreo y Logs

### Health Checks
- Backend: `GET /api/health`
- Frontend: Página de estado en desarrollo
- Base de datos: Verificación de conexión automática

### Logs
```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Logs en tiempo real
docker-compose logs -f backend
```

## 🚢 Despliegue en Producción

### Variables de Producción
```bash
FLASK_ENV=production
DATABASE_URL=postgresql://prod_user:secure_pass@prod_host:5432/prod_db
SECRET_KEY=production_secret_key
JWT_SECRET_KEY=production_jwt_secret
```

### Consideraciones
- Configurar SSL/TLS para HTTPS
- Usar PostgreSQL gestionado (AWS RDS, Google Cloud SQL)
- Configurar Redis para cache y sesiones
- Implementar load balancer para escalabilidad
- Configurar backups automáticos
- Monitoring con herramientas como Sentry o DataDog

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -am 'Agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades:
- Crear issue en el repositorio
- Email: support@schedulesapp.com
- Documentación: Consultar `swagger.yaml`

---

**Desarrollado con ❤️ por el equipo de SchedulesApp**