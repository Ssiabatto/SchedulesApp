# 🚢 SchedulesApp — Guía de Despliegue

Esta guía cubre escenarios típicos de despliegue para correr el sistema en una sola PC, en una LAN o contra una base de datos remota. Incluye pasos para Windows (cmd.exe), Docker y opciones sin Docker.

## ✅ Requisitos

- Windows 10/11 o Linux/Mac
- Para Docker: Docker Desktop + Docker Compose
- Para nativo: Python 3.11+, Node.js 18+, PostgreSQL 13+

## 🔧 Variables de entorno clave

- Backend: DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY, FLASK_ENV
- Frontend: NEXT_PUBLIC_API_URL

Usa .env (raíz) y frontend/.env.local. Ejemplos en .env.example y frontend/.env.example.

## Opción A — Todo con Docker (recomendado para una sola máquina)

1. copy .env.example .env
2. copy frontend\.env.example frontend\.env.local
3. docker-compose up --build -d
4. docker-compose exec backend python init_db.py
5. docker-compose exec backend python create_demo_user.py
6. Acceso: Frontend http://localhost:3000 — API http://localhost:5000/api

Notas:
- DATABASE_URL en .env debe usar host db cuando corra con Docker: postgresql://user:password@db:5432/gestion_turnos_vigilantes
- El test de integración: python test_integration.py (API_BASE_URL opcional)

## Opción B — DB en Docker; Backend y Frontend nativos

1. Levanta solo la DB: docker-compose up -d db
2. Configura .env con DATABASE_URL apuntando a localhost: postgresql://user:password@localhost:5432/gestion_turnos_vigilantes
3. Backend (en backend/):
   - python -m venv venv && venv\Scripts\activate
   - pip install -r requirements.txt
   - python init_db.py && python create_demo_user.py
   - python app/main.py  (API en http://localhost:5000)
4. Frontend (en frontend/):
   - npm install
   - NEXT_PUBLIC_API_URL=http://localhost:5000/api en .env.local
   - npm run dev  (http://localhost:3000)

## Opción C — Todo nativo (sin Docker)

1. Instala PostgreSQL y crea la BD gestion_turnos_vigilantes
2. Ajusta DATABASE_URL en .env para localhost
3. Sigue los pasos del Backend y Frontend como en Opción B (3 y 4)

## Opción D — Backend como .exe (solo backend empaquetado)

Escenario: quieres un ejecutable del backend en Windows y correr el frontend con Node o como estático.

1. Backend .exe con PyInstaller (desde backend/):
   - venv\Scripts\activate
   - pip install -r requirements.txt
   - pip install pyinstaller
   - pyinstaller --onefile --name SchedulesBackend --add-data "app;app" app/main.py
   - El binario estará en dist\SchedulesBackend.exe
2. Variables de entorno:
   - Crea un archivo .env junto a SchedulesBackend.exe o define variables en el sistema (DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY)
3. Base de datos:
   - Usa PostgreSQL local o remoto. Para remoto: DATABASE_URL=postgresql://user:password@host:5432/prod_db
4. Frontend:
   - Desarrollo: npm run dev
   - Producción: npm run build && npm run start, o exporta estático y sírvelo detrás de Nginx/IIS

Notas:
- El .exe lanza el API Flask en el puerto 5000 por defecto. Cambia via variable PORT si tu main.py la soporta, o usa un proxy frontal.

## Cambiar a Base de Datos Remota (producción)

1. Consigue el string de conexión del proveedor (RDS, Cloud SQL u on-premise):
   - Formato: postgresql://usuario:contraseña@host:puerto/nombre
2. Actualiza DATABASE_URL:
   - En .env (Docker o nativo) o en las variables del sistema (si usas .exe)
3. Reinicia los servicios:
   - Docker: docker-compose restart backend (o up --build)
   - Nativo: reinicia el proceso Python o el .exe
4. Verifica conectividad:
   - python test_integration.py

## Redes y puertos

- API: 5000/tcp
- Frontend: 3000/tcp
- PostgreSQL: 5432/tcp
- Redis: 6379/tcp (opcional)

Abre puertos en firewall si corresponde. Para LAN, expón NEXT_PUBLIC_API_URL con IP de la máquina: p.ej. http://192.168.0.10:5000/api y arranca el frontend con ese valor.

## Checklist de despliegue

- [ ] Variables de entorno definidas y secretas seguras
- [ ] Base de datos accesible y migraciones/tablas creadas
- [ ] Usuario admin creado (create_demo_user.py)
- [ ] API accesible en /api/health
- [ ] Frontend apunta al API correcto (NEXT_PUBLIC_API_URL)
- [ ] Logs sin errores críticos

## Troubleshooting rápido

- Puertos ocupados: netstat -ano | findstr :5000 (Windows)
- DB vacía: re-ejecuta init_db.py y create_demo_user.py
- CORS/token: revisa JWT_SECRET_KEY y reloj del sistema

## Notas de producción

- Usa PostgreSQL gestionado y backups automatizados
- HTTPS/SSL con proxy inverso (Nginx/Traefik/IIS)
- Supervisar procesos (systemd, NSSM, PM2 para frontend Node)
- Observabilidad: Sentry/Datadog/Elastic
