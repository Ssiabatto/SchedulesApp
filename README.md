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

## ⚡ Inicio Rápido (Windows)

Si quieres validar rápido que todo funciona en Windows usando Docker:

1) copy .env.example .env y copy frontend\.env.example frontend\.env.local
2) docker-compose up --build -d
3) docker-compose exec backend python init_db.py && docker-compose exec backend python create_demo_user.py
4) python test_integration.py  (usa http://localhost:5000/api por defecto)
5) Abre http://localhost:3000 y entra con admin / admin123

## 🚀 Instalación y Configuración

### Opción 1: Docker (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd SchedulesApp
```

2. **Configurar variables de entorno**
```bash
# Windows
copy .env.example .env
copy frontend\.env.example frontend\.env.local

# Linux/Mac
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
# Windows
copy .env.example .env.local

# Linux/Mac
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

Para despliegue paso a paso (Docker, nativo, .exe y base de datos remota), ver: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📋 Historial de Versiones

El desarrollo completo del proyecto está documentado en [CHANGELOG.md](CHANGELOG.md), donde se puede consultar:

- **v1.0.0** (2025-07-09): Versión de producción con documentación completa, testing y seguridad
- **v0.9.0** (2025-06-20): Beta con PostgreSQL, Clean Architecture y UI completa
- **v0.8.0** (2025-05-25): Alpha con fundamentos backend y frontend básico
- **Versiones anteriores**: Planificación, diseño y análisis de requisitos

Ver [CHANGELOG.md](CHANGELOG.md) para detalles completos de cada versión.

## 📘 Guía Completa de Instalación y Ejecución

### 📋 Prerrequisitos

**Software requerido:**
- **Docker & Docker Compose** (recomendado)
- **Git** para clonar el repositorio
- **Python 3.11+** (si ejecutas localmente)
- **Node.js 18+** (si ejecutas localmente)
- **PostgreSQL 13+** (si ejecutas localmente)

**Verificar instalaciones:**
```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Python
python --version

# Verificar Node.js
node --version
npm --version
```

### 🐳 Opción 1: Ejecución con Docker (Recomendado)

#### Paso 1: Clonar el Repositorio
```bash
# Clonar el proyecto
git clone <repository-url>
cd SchedulesApp
```

#### Paso 2: Configurar Variables de Entorno

**2.1. Backend (.env)**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

**Editar el archivo .env:**
```bash
# Windows - abrir con Notepad
notepad .env

# Linux/Mac - abrir con nano/vim
nano .env
# o vim .env
```

**Reemplazar los valores de ejemplo:**
```bash
# Generar claves secretas seguras
SECRET_KEY=tu_clave_secreta_super_segura_aqui_32_caracteres
JWT_SECRET_KEY=tu_clave_jwt_diferente_muy_segura_aqui_32_chars

# Para desarrollo, puedes mantener estos valores:
DATABASE_URL=postgresql://user:password@localhost:5432/gestion_turnos_vigilantes
CELERY_BROKER_URL=redis://localhost:6379/0
FLASK_ENV=development
```

**2.2. Frontend (.env.local)**
```bash
# Windows
copy frontend\.env.example frontend\.env.local

# Linux/Mac
cp frontend/.env.example frontend/.env.local
```

**Editar frontend/.env.local:**
```bash
# Este valor generalmente no necesita cambios para desarrollo local
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

#### Paso 3: Generar Claves Secretas Seguras

**Generar SECRET_KEY y JWT_SECRET_KEY:**
```bash
# Método 1: Usando Python
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"

# Método 2: Usando OpenSSL (Linux/Mac)
openssl rand -hex 32

# Método 3: Generador online (NO recomendado para producción)
# Ir a: https://generate-secret.vercel.app/32
```

**Copiar y pegar las claves generadas en tu archivo .env**

#### Paso 4: Levantar la Aplicación
```bash
# Construir y levantar todos los servicios
docker-compose up --build -d

# Verificar que todos los servicios estén corriendo
docker-compose ps
```

**Deberías ver 4 servicios activos:**
- `schedulesapp_backend_1` (Puerto 5000)
- `schedulesapp_frontend_1` (Puerto 3000) 
- `schedulesapp_db_1` (Puerto 5432)
- `schedulesapp_redis_1` (Puerto 6379)

#### Paso 5: Inicializar Base de Datos
```bash
# Crear las tablas de la base de datos
docker-compose exec backend python init_db.py

# Crear usuario demo para pruebas
docker-compose exec backend python create_demo_user.py
```

#### Paso 6: Verificar Instalación
```bash
# Ejecutar tests de integración
python test_integration.py

# Si todo está bien, deberías ver:
# 🎉 All tests passed! The API is working correctly.
```

#### Paso 7: Acceder a la Aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000/api
- **Health Check**: http://localhost:5000/api/health

**Credenciales de prueba:**
- Username: `admin`
- Password: `admin123`

### 💻 Opción 2: Ejecución Local (Desarrollo)

#### Configuración del Backend

**1. Crear entorno virtual Python:**
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**2. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**3. Configurar PostgreSQL local:**
```bash
# Instalar PostgreSQL en tu sistema
# Windows: Descargar desde https://www.postgresql.org/download/windows/
# Linux: sudo apt-get install postgresql postgresql-contrib
# Mac: brew install postgresql

# Crear base de datos
createdb gestion_turnos_vigilantes

# O usando psql:
psql -U postgres
CREATE DATABASE gestion_turnos_vigilantes;
\q
```

**4. Configurar variables de entorno:**
```bash
# Copiar archivo de ejemplo
# Windows
copy ..\.env.example .env

# Linux/Mac
cp ../.env.example .env

# Editar .env con tu configuración local
# Actualizar DATABASE_URL con tus credenciales de PostgreSQL
DATABASE_URL=postgresql://tu_usuario:tu_password@localhost:5432/gestion_turnos_vigilantes
```

**5. Inicializar base de datos:**
```bash
python init_db.py
python create_demo_user.py
```

**6. Ejecutar backend:**
```bash
python app/main.py
# El backend estará disponible en http://localhost:5000
```

#### Configuración del Frontend

**1. Instalar dependencias (nueva terminal):**
```bash
cd frontend
npm install
```

**2. Configurar variables de entorno:**
```bash
# Windows
copy .env.example .env.local

# Linux/Mac
cp .env.example .env.local

# Editar .env.local si es necesario (generalmente no es necesario)
```

**3. Ejecutar frontend:**
```bash
npm run dev
# El frontend estará disponible en http://localhost:3000
```

### 🔧 Obtener Variables de Entorno

#### SECRET_KEY y JWT_SECRET_KEY

**Opción A: Usando Python (Recomendado)**
```python
# Ejecutar en terminal Python
python -c "
import secrets
print('SECRET_KEY=' + secrets.token_hex(32))
print('JWT_SECRET_KEY=' + secrets.token_hex(32))
"
```

**Opción B: Usando Node.js**
```javascript
// Ejecutar en terminal Node.js
node -e "
const crypto = require('crypto');
console.log('SECRET_KEY=' + crypto.randomBytes(32).toString('hex'));
console.log('JWT_SECRET_KEY=' + crypto.randomBytes(32).toString('hex'));
"
```

**Opción C: Generador online (solo para desarrollo)**
- Ir a: https://generate-secret.vercel.app/32
- **⚠️ NUNCA usar generadores online para producción**

#### DATABASE_URL

**Formato:**
```
postgresql://usuario:contraseña@host:puerto/nombre_base_datos
```

**Ejemplos:**
```bash
# Desarrollo local
DATABASE_URL=postgresql://postgres:mipassword@localhost:5432/gestion_turnos_vigilantes

# Docker (usar esto cuando ejecutes con docker-compose)
DATABASE_URL=postgresql://user:password@db:5432/gestion_turnos_vigilantes

# Producción (ejemplo con servicio en la nube)
DATABASE_URL=postgresql://prod_user:secure_pass@your-db-host.com:5432/prod_db
```

### 🛠️ Comandos Útiles

#### Docker
```bash
# Ver logs de servicios
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Reiniciar un servicio específico
docker-compose restart backend

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes (⚠️ elimina datos de DB)
docker-compose down -v

# Reconstruir servicios
docker-compose up --build
```

#### Base de Datos
```bash
# Conectar a PostgreSQL (Docker)
docker-compose exec db psql -U user -d gestion_turnos_vigilantes

# Conectar a PostgreSQL (local)
psql -U postgres -d gestion_turnos_vigilantes

# Ver tablas
\dt

# Salir de psql
\q
```

#### Tests
```bash
# Tests de integración
python test_integration.py

# Verificar health check
curl http://localhost:5000/api/health

# Test de login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 🚨 Solución de Problemas Comunes

#### Error: "cp no se reconoce como comando"
```bash
# Estás en Windows, usa:
copy .env.example .env
# En lugar de:
cp .env.example .env
```

#### Error: "Docker Desktop no está ejecutándose"
```bash
# Error: "unable to get image" o "cannot find file specified"
# Solución:
# 1. Abrir Docker Desktop desde el menú Inicio
# 2. Esperar a que se inicialice completamente
# 3. Verificar: docker ps
# 4. Reintentar: docker-compose up --build -d
```

#### Error: "Puerto ya en uso"
```bash
# Verificar qué proceso usa el puerto
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000

# Parar el proceso o cambiar puerto en docker-compose.yml
```

#### Error: "Base de datos no existe"
```bash
# Recrear base de datos
docker-compose down -v
docker-compose up -d db
docker-compose exec backend python init_db.py
```

#### Error: "Claves secretas inválidas"
```bash
# Regenerar claves
python -c "import secrets; print(secrets.token_hex(32))"
# Actualizar en .env y reiniciar
```

### 📚 Próximos Pasos

1. **Leer la documentación**: Consultar [TESTING_GUIDE.md](TESTING_GUIDE.md)
2. **Explorar la API**: Revisar [swagger.yaml](swagger.yaml)
3. **Entender la arquitectura**: Ver estructura del proyecto arriba
4. **Contribuir**: Seguir las guías de contribución

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