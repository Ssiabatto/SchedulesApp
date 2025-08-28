# 🧪 SchedulesApp - Guía de Testing

## 📋 Resumen de Testing

Esta guía explica cómo probar completamente el funcionamiento del sistema SchedulesApp, tanto frontend como backend, para asegurar que todos los componentes funcionen correctamente.

## 🚀 Pre-requisitos para Testing

### Software Requerido
- **Docker & Docker Compose** (para método recomendado)
- **Python 3.11+** y **Node.js 18+** (para testing local)
- **PostgreSQL 13+** (si se ejecuta localmente)
- **Git** para clonar el repositorio

### Verificación de Pre-requisitos
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

## 🔧 Configuración de Entorno de Testing

### Método 1: Docker (Recomendado)

1. **Clonar y configurar proyecto**
```bash
git clone <repository-url>
cd SchedulesApp

# Windows
copy .env.example .env
copy frontend\.env.example frontend\.env.local

# Linux/Mac
cp .env.example .env
cp frontend/.env.example frontend/.env.local
```

2. **Levantar servicios**
```bash
docker-compose up --build -d
```

3. **Verificar que todos los servicios estén corriendo**
```bash
docker-compose ps
```

Deberías ver 4 servicios running:
- `schedulesapp_backend_1`
- `schedulesapp_frontend_1` 
- `schedulesapp_db_1`
- `schedulesapp_redis_1`

4. **Inicializar base de datos**
```bash
docker-compose exec backend python init_db.py
docker-compose exec backend python create_demo_user.py
```

### Método 2: Local Development

1. **Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. **Database Setup**
```bash
# Crear base de datos PostgreSQL
createdb gestion_turnos_vigilantes

# Configurar DATABASE_URL en .env
# Windows - editar manualmente o usar:
notepad .env

# Linux/Mac
nano .env
# o vim .env

python init_db.py
python create_demo_user.py
```

3. **Frontend Setup**
```bash
cd frontend
npm install

# Configurar variables de entorno
# Windows
copy .env.example .env.local

# Linux/Mac  
cp .env.example .env.local

npm run build  # Verificar que el build sea exitoso
```

## 🧪 Tests Automatizados

### 1. Test de Integración API

El script `test_integration.py` verifica los endpoints principales:

```bash
python test_integration.py

# Opcional: cambiar la URL base si el backend corre en otro host/puerto
# Windows cmd.exe
set API_BASE_URL=http://127.0.0.1:5000/api && python test_integration.py
```

**Qué verifica:**
- ✅ Health check del API (`/api/health`)
- ✅ Registro de usuario (`/api/auth/register`)
- ✅ Login de usuario (`/api/auth/login`)
- ✅ Endpoint protegido (`/api/auth/protected`)

**Resultado esperado (resumen abreviado):**
```
Starting SchedulesApp Integration Tests
--------------------------------------------------
- Testing health check...
- Testing user registration...
- Testing user login...
- Testing protected endpoint...
--------------------------------------------------
Test Results: 4/4 tests passed
All tests passed! The API is working correctly.
```

### 2. Test de Base de Datos

Verificar conexión y estructura de la base de datos:

```bash
# Usando Docker
docker-compose exec db psql -U user -d gestion_turnos_vigilantes -c "\dt"

# Local
psql -U user -d gestion_turnos_vigilantes -c "\dt"
```

**Tablas esperadas:**
- usuarios
- vigilantes  
- edificios
- asignaciones_turnos
- certificaciones_vigilantes
- tipos_turnos
- planilla_turnos
- novedades
- Y 7 tablas adicionales del schema PostgreDB.sql

## 🌐 Tests Manuales Frontend

### 1. Acceso a la Aplicación

1. **Abrir navegador**
```
http://localhost:3000
```

2. **Verificar página de inicio**
- ✅ La página carga sin errores
- ✅ Se muestra el formulario de login
- ✅ CSS y estilos se aplican correctamente

### 2. Test de Autenticación

1. **Login con credenciales demo**
```
Username: admin
Password: admin123
```

2. **Verificaciones:**
- ✅ Login exitoso redirige al dashboard
- ✅ Token JWT se almacena en localStorage
- ✅ Usuario logueado se muestra en la interfaz

3. **Test de sesión inválida**
- Intentar login con credenciales incorrectas
- ✅ Debe mostrar mensaje de error
- ✅ No debe redirigir al dashboard

### 3. Test de Navegación

1. **Dashboard Principal**
- ✅ Sidebar se despliega correctamente
- ✅ Menú de navegación funciona
- ✅ Cards de resumen se muestran

2. **Módulo de Vigilantes** (`/guards`)
- ✅ Tabla de vigilantes carga
- ✅ Botones de acción están presentes
- ✅ Filtros funcionan correctamente

3. **Módulo de Edificios** (`/buildings`)  
- ✅ Lista de edificios se muestra
- ✅ Formulario de creación funciona
- ✅ Acciones CRUD disponibles

4. **Módulo de Contratos** (`/contracts`)
- ✅ Gestión de contratos operativa
- ✅ Formularios de validación funcionan

5. **Módulo de Reportes** (`/reports`)
- ✅ Filtros de reporte funcionan
- ✅ Exportación de datos operativa

### 4. Test de Responsividad

1. **Desktop (1920x1080)**
- ✅ Layout se adapta correctamente
- ✅ Sidebar completo visible

2. **Tablet (768x1024)**
- ✅ Sidebar se colapsa apropiadamente
- ✅ Contenido se reorganiza

3. **Mobile (375x667)**
- ✅ Navegación móvil funciona
- ✅ Tablas son scrolleables
- ✅ Formularios son usables

## 🔗 Tests de API Backend

### 1. Health Check

```bash
curl http://localhost:5000/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy", 
  "message": "API is running",
  "timestamp": "2025-01-09T..."
}
```

### 2. Autenticación

**Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "access_token": "eyJ...",
  "user": {
    "id": 1,
    "username": "admin", 
    "role": "operador_supervisor",
    "full_name": "Administrador Sistema"
  }
}
```

**Test con credenciales inválidas:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "wrong"}'
```

**Respuesta esperada:**
```json
{
  "success": false,
  "message": "Invalid username or password"
}
```

### 3. Endpoints Protegidos

**Usar token obtenido del login:**
```bash
TOKEN="eyJ..."  # Token del login anterior

curl -X GET http://localhost:5000/api/auth/protected \
  -H "Authorization: Bearer $TOKEN"
```

**Respuesta esperada:**
```json
{
  "success": true,
  "message": "Access granted",
  "user": {
    "username": "admin",
    "user_id": 1,
    "role": "operador_supervisor"
  }
}
```

### 4. Test sin Token

```bash
curl -X GET http://localhost:5000/api/auth/protected
```

**Respuesta esperada:**
```json
{
  "msg": "Missing Authorization Header"
}
```

## 🏗️ Tests de Infraestructura

### 1. Test de Docker

**Verificar logs de servicios:**
```bash
# Backend logs
docker-compose logs backend

# Frontend logs  
docker-compose logs frontend

# Database logs
docker-compose logs db

# Redis logs
docker-compose logs redis
```

**No debe haber errores críticos en los logs.**

### 2. Test de Base de Datos

**Conectividad:**
```bash
docker-compose exec db psql -U user -d gestion_turnos_vigilantes -c "SELECT version();"
```

**Verificar usuario demo:**
```bash
docker-compose exec db psql -U user -d gestion_turnos_vigilantes -c "SELECT * FROM usuarios WHERE nombre_usuario='admin';"
```

### 3. Test de Redis

```bash
docker-compose exec redis redis-cli ping
```

**Respuesta esperada:** `PONG`

## 🐛 Resolución de Problemas Comunes

### Backend No Responde

1. **Verificar logs:**
```bash
docker-compose logs backend
```

2. **Verificar puerto:**
```bash
curl http://localhost:5000/api/health
```

3. **Reiniciar servicio:**
```bash
docker-compose restart backend
```

### Frontend No Carga

1. **Verificar logs:**
```bash
docker-compose logs frontend
```

2. **Verificar puerto:**
```bash
curl http://localhost:3000
```

3. **Reconstruir:**
```bash
docker-compose up --build frontend
```

### Base de Datos Sin Datos

1. **Re-inicializar:**
```bash
docker-compose exec backend python init_db.py
docker-compose exec backend python create_demo_user.py
```

2. **Verificar conexión:**
```bash
docker-compose exec db psql -U user -d gestion_turnos_vigilantes -c "\dt"
```

### Error de Autenticación

1. **Verificar variables de entorno:**
```bash
# Windows
type .env | findstr JWT_SECRET_KEY

# Linux/Mac
cat .env | grep JWT_SECRET_KEY
```

2. **Limpiar localStorage del navegador**

3. **Verificar usuario demo existe:**
```bash
docker-compose exec db psql -U user -d gestion_turnos_vigilantes -c "SELECT * FROM usuarios;"
```

## ✅ Checklist Completo de Testing

### Infraestructura
- [ ] Docker Compose levanta todos los servicios
- [ ] PostgreSQL acepta conexiones
- [ ] Redis responde a ping
- [ ] Logs no muestran errores críticos

### Backend API
- [ ] Health check responde
- [ ] Login con credenciales válidas funciona
- [ ] Login con credenciales inválidas falla apropiadamente
- [ ] Endpoints protegidos requieren autenticación
- [ ] Token JWT se genera correctamente

### Frontend
- [ ] Página principal carga sin errores
- [ ] Login funciona y redirige al dashboard
- [ ] Navegación entre secciones operativa
- [ ] Sidebar responsive funciona
- [ ] Tablas y formularios se renderizan correctamente

### Integración
- [ ] Frontend se comunica con backend
- [ ] Datos se persisten en base de datos
- [ ] Autenticación funciona end-to-end
- [ ] Errores se manejan apropiadamente

### Funcionalidad de Negocio
- [ ] Gestión de vigilantes operativa
- [ ] Gestión de edificios operativa
- [ ] Sistema de roles funciona
- [ ] Validaciones de formularios operan

## 📊 Métricas de Performance

### Backend
- Health check debe responder en < 200ms
- Login debe completarse en < 500ms
- Consultas a base de datos < 1s

### Frontend  
- Página inicial debe cargar en < 3s
- Navegación entre secciones < 1s
- Formularios deben responder inmediatamente

## 🎯 Conclusión

Si todos los tests pasan exitosamente, el sistema está listo para uso en desarrollo. Para producción, se recomienda:

1. Configurar SSL/HTTPS
2. Usar base de datos gestionada
3. Implementar monitoring y alertas
4. Configurar backups automáticos
5. Realizar tests de carga y estrés

---

**¡Happy Testing!** 🧪✨
