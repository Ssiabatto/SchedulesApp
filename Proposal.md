# 1. Descripción del Problema y Solución Propuesta

## 🛑 Problema

La planificación y gestión de turnos de vigilancia en múltiples edificios presenta grandes retos:

- Asignaciones manuales ineficientes
- Dificultad para reemplazos por ausencias o emergencias
- Inexactitud en el cálculo de horas trabajadas y recargos
- Reportes financieros imprecisos o inexistentes
- Falta de automatización en la planilla mensual

## 💡 Solución Propuesta

Un sistema de software web que automatice:

- Enrolamiento de vigilantes y edificios
- Generación inteligente de turnos basada en reglas de negocio
- Gestión de contingencias (reemplazos, ausencias, incapacidades)
- Cálculo de horas normales, extras y festivas
- Generación de reportes exportables

---

# 2. Requisitos del Sistema

## ✅ Requisitos Funcionales

- Registro y edición de vigilantes, edificios y usuarios
- Registro de contratos, horarios, habilidades y certificaciones
- Asignación automática de turnos según proximidad, descanso y disponibilidad
- Visualización de planillas por edificio/día/semana/mes
- Registro de ausencias, incapacidades, permisos y novedades
- Reasignación automática ante contingencias
- Registro y cálculo automático de horas normales y extras
- Generación de reportes por vigilante y por edificio
- Exportación de reportes a PDF y Excel
- Control de acceso por roles (Operador y Auxiliar)
- Validación de horas mínimas de descanso
- Registro histórico y backups trimestrales
- Restauración desde backup

## 🔒 Requisitos No Funcionales

- **Seguridad:** Contraseñas encriptadas con bcrypt
- **Rendimiento:** Respuestas rápidas para consultas masivas
- **Escalabilidad:** Soporte a múltiples edificios y usuarios simultáneos
- **Disponibilidad:** Acceso web desde distintos dispositivos
- **Usabilidad:** Interfaz responsiva y fácil de usar
- **Mantenibilidad:** Código modular y documentado
- **Respaldo:** Eliminación automática tras descarga del backup
- **Compatibilidad:** Integración con API de Odoo

---

# 3. Segmentación del Sistema en Módulos

| Módulo | Funcionalidad Principal | No Funcional | Responsabilidad | Relación |
|--------|------------------------|--------------|-----------------|----------|
| **1. Enrolamiento y Datos Base** | Registro de vigilantes, edificios, usuarios | Validaciones, encriptación | Administra información base | Base para turnos y contingencias |
| **2. Planificación de Turnos** | Generación automática de planilla | Filtros avanzados | Asignaciones mensuales óptimas | Usa datos del módulo 1, envía al 4 |
| **3. Gestión de Contingencias** | Registrar novedades, buscar reemplazos | Algoritmo robusto | Cobertura ante imprevistos | Usa módulo 2, afecta módulo 4 |
| **4. Registro y Liquidación de Horas** | Cálculo automático de horas y recargos | Precisión en fechas/horarios | Consolidar datos para reportes | Recibe datos de 2 y 3 |
| **5. Reportes y Exportación** | Reportes por vigilante/edificio, exportación | Generación rápida | Informar a operador y auxiliar | Usa datos del 4 |
| **6. Seguridad y Control de Acceso** | Autenticación por roles, sesiones | JWT y bcrypt | Garantizar integridad | Aplica a todos los módulos |

---

# 4. Planeación del Desarrollo del Proyecto

## 🗂️ Épicas del Proyecto

El desarrollo se organiza en tres grandes bloques funcionales:

1. **Enrolamiento y configuración base:**  
   Registro de vigilantes, edificios, usuarios y configuración inicial de contratos, horarios y roles.

2. **Planificación y gestión de contingencias:**  
   Automatización de la asignación de turnos, manejo de ausencias, reemplazos y novedades, asegurando cobertura eficiente y cumplimiento de reglas.

3. **Registro de horas, reportes y exportación:**  
   Consolidación de la información de turnos, cálculo automático de horas y recargos, y generación de reportes exportables para gestión y análisis.

---

## 👤 Historias de Usuario

- *Como operador, quiero registrar un nuevo vigilante con todos sus datos personales y laborales para que pueda ser asignado a turnos.*
- *Como operador, quiero editar la información de un vigilante o edificio para mantener los datos actualizados.*
- *Como operador, quiero registrar contratos, horarios y certificaciones para asegurar el cumplimiento de requisitos legales y operativos.*
- *Como operador, quiero generar la planilla del mes automáticamente para reducir errores y ahorrar tiempo.*
- *Como operador, quiero visualizar la planilla por edificio, día, semana o mes para facilitar la gestión.*
- *Como operador, quiero registrar una ausencia y que el sistema proponga un reemplazo para no dejar vacío el turno.*
- *Como operador, quiero reasignar turnos automáticamente ante contingencias para mantener la cobertura.*
- *Como operador, quiero registrar y calcular automáticamente las horas normales, extras y festivas para una liquidación precisa.*
- *Como operador, quiero generar reportes por vigilante y por edificio para análisis y control.*
- *Como auxiliar administrativo, quiero exportar a Excel o PDF el reporte mensual de horas trabajadas por edificio para enviarlo a contabilidad.*
- *Como usuario, quiero acceder al sistema de forma segura según mi rol para proteger la información.*
- *Como administrador, quiero realizar backups y restauraciones para garantizar la seguridad de los datos.*

---

# 5. Metodología de desarrollo

El proyecto se desarrollará de forma **iterativa e incremental**, permitiendo entregar valor de manera continua y recibir retroalimentación temprana del cliente.

### Iteraciones

- Cada iteración (sprint) tiene una duración de **2 semanas (14 días)**.
- Al final de cada sprint se realiza una revisión con el cliente para validar avances y ajustar prioridades.

### Incrementos Funcionales

#### 🚀 Incremento 1: MVP Funcional (Semana 1-2)
- Registro y edición de vigilantes, edificios y usuarios.
- Login seguro con JWT y bcrypt.
- Asignación manual de turnos.
- Visualización de la planilla en un calendario interactivo (FullCalendar).

#### 🚀 Incremento 2: Planificación Automática y Contingencias (Semana 3-4)
- Algoritmo de asignación automática de turnos.
- Registro de novedades: ausencias, incapacidades, vacaciones.
- Sugerencia automática de reemplazos.
- Filtros avanzados en el calendario por edificio y vigilante.

#### 🚀 Incremento 3: Reportes, Cálculo y Backups (Semana 5-6)
- Registro de horas trabajadas y cálculo automático de liquidación.
- Exportación de reportes a PDF y Excel (WeasyPrint, Pandas, XlsxWriter).
- Backup trimestral y restauración automática.
- Eliminación de registros descargados según política de respaldo.

---

# 🏗️ Recomendaciones Técnicas

## 🔧 Arquitectura

El sistema se implementará utilizando una arquitectura **Clean Architecture** (o Hexagonal) combinada con el patrón **MVC** para asegurar un desarrollo robusto, escalable y fácil de mantener. Esta arquitectura permite separar claramente la lógica de negocio, la orquestación de flujos, la infraestructura y la interfaz, facilitando la integración con sistemas externos y la realización de pruebas.

- **Domain Layer:** Aquí se concentra la lógica de negocio pura, como el algoritmo de asignación de turnos y la liquidación de horas. Esta capa es independiente de frameworks y tecnologías externas, lo que facilita su reutilización y testeo.
- **Application Layer:** Se encarga de la orquestación de los flujos de la aplicación, coordinando las operaciones entre la lógica de negocio y las interfaces externas.
- **Infrastructure Layer:** Incluye la gestión de la base de datos (PostgreSQL), integración con APIs externas (como Odoo), servicios de correo y módulos de exportación de reportes.
- **Interface Layer:** Provee una API REST desarrollada en Flask para el backend y una SPA en React para el frontend, asegurando una experiencia de usuario moderna y responsiva.

**Ventajas de esta arquitectura:**  
- Permite desacoplar componentes y facilita el mantenimiento.
- Hace posible la integración sencilla con sistemas externos como Odoo.
- Mejora la escalabilidad y la capacidad de realizar pruebas unitarias y de integración.

---

## 🧱 Base de Datos

Se utilizará **PostgreSQL** como sistema de gestión de base de datos relacional, por su robustez, escalabilidad y soporte avanzado para relaciones complejas.  
- **Modelo relacional:** Permite estructurar y relacionar eficientemente la información de vigilantes, turnos, edificios y novedades.
- **Concurrencia y rendimiento:** PostgreSQL soporta múltiples usuarios y operaciones simultáneas sin degradar el rendimiento.
- **Soporte geoespacial (opcional):** Con PostGIS, se puede agregar funcionalidad de geolocalización para optimizar asignaciones por proximidad.
- **Herramientas de administración:** Se recomienda el uso de PgAdmin 4 para la gestión visual de la base de datos.

---

## 🌐 Tecnologías Recomendadas

| Capa             | Tecnología                               | Justificación                                        |
|------------------|------------------------------------------|------------------------------------------------------|
| Backend          | Flask + SQLAlchemy                       | Framework ligero y flexible, ideal para APIs REST. ORM potente para manejo de datos. |
| Frontend         | **Next.js 15** + Tailwind + Radix UI     | Framework React moderno con App Router, SSR y optimizaciones automáticas. |
| Base de Datos    | PostgreSQL                               | Robusta, escalable y ampliamente soportada.          |
| Autenticación    | Flask-JWT-Extended + bcrypt              | Seguridad avanzada y control de sesiones.            |
| Reportes         | Flask + Pandas + WeasyPrint / XlsxWriter | Generación de reportes PDF y Excel de alta calidad.  |
| Integración Odoo | REST API via OAuth2                      | Comunicación segura y estándar con sistemas externos.|

---

## 📦 Otras Herramientas y Prácticas

- **Celery + Redis:** Para la ejecución de tareas programadas y asíncronas, como generación de reportes, backups automáticos y envío de notificaciones.
- **Docker y Docker Compose:** Para el despliegue y la orquestación de todos los servicios (API, base de datos, Redis), asegurando portabilidad y facilidad de configuración en distintos entornos.
- **Git + GitHub/GitLab:** Control de versiones y colaboración en equipo, con flujos de trabajo basados en ramas y revisiones de código.
- **Postman:** Testing y documentación de la API REST, facilitando la validación de endpoints y la integración con otros sistemas.

---

## 🛠️ Backend (Flask + Ecosistema)

| Herramienta        | Propósito                      | Licencia   | Comentario                                          |
|--------------------|--------------------------------|------------|-----------------------------------------------------|
| Flask              | Framework web backend          | BSD        | Ligero y extensible. Ideal para API REST.           |
| SQLAlchemy         | ORM para bases de datos        | MIT        | Mapea clases Python a tablas SQL.                   |
| Flask-Migrate      | Migraciones de base de datos   | MIT        | Basado en Alembic. Control de versiones de esquema. |
| Flask-JWT-Extended | Autenticación JWT              | MIT        | Manejo seguro de autenticación.                     |
| bcrypt             | Encriptación de contraseñas    | Apache 2.0 | Mucho más seguro que MD5/SHA1.                      |
| Celery             | Ejecución de tareas asíncronas | BSD        | Ideal para tareas de fondo como reportes, backups.  |
| Redis              | Cola de tareas / Cache         | BSD        | Usado por Celery. Muy rápido.                       |

---

## 💾 Base de Datos

| Herramienta | Propósito                        | Licencia   | Comentario                                   |
|-------------|----------------------------------|------------|----------------------------------------------|
| PostgreSQL  | Base de datos relacional         | PostgreSQL | Robusta, escalable y 100% libre.             |
| PgAdmin 4   | Interfaz gráfica para PostgreSQL | PostgreSQL | Administra tu base de datos con UI amigable. |

---

## 🎨 Frontend (Next.js + Ecosistema)

| Herramienta          | Propósito                       | Licencia | Comentario                                     |
|----------------------|---------------------------------|----------|------------------------------------------------|
| **Next.js 15**       | Framework React full-stack     | MIT      | App Router, SSR, optimizaciones automáticas    |
| **Tailwind CSS v4**  | Estilos rápidos y responsivos   | MIT      | Utiliza clases utilitarias modernas            |
| **Radix UI**         | Componentes UI accesibles       | MIT      | Base sólida para componentes complejos         |
| **shadcn/ui**        | Sistema de componentes          | MIT      | Componentes pre-construidos con Radix          |
| **Lucide React**     | Iconografía                     | MIT      | Iconos SVG optimizados para React              |

---

## 📈 Reportes y Exportación

| Herramienta | Propósito                | Licencia | Comentario                                  |
|-------------|--------------------------|----------|---------------------------------------------|
| Pandas      | Análisis de datos/tablas | BSD      | Muy potente para manejar reportes.          |
| XlsxWriter  | Exportar a Excel         | BSD      | Permite crear archivos Excel complejos.     |
| WeasyPrint  | Convertir HTML a PDF     | BSD      | Genera PDFs de alta calidad desde HTML/CSS. |

---

## 🧪 Testing, API y Control de Versiones

| Herramienta     | Propósito            | Licencia                  | Comentario                                       |
|-----------------|----------------------|---------------------------|--------------------------------------------------|
| Postman         | Testeo de APIs       | Gratuita (versión básica) | Herramienta muy útil para probar endpoints.      |
| Git             | Control de versiones | GPL                       | Indispensable para manejar versiones del código. |
| GitHub / GitLab | Repositorio remoto   | Gratuito (planes básicos) | Para colaboración y despliegue.                  |

---

## 🚀 Despliegue y Entornos

| Herramienta    | Propósito                                    | Licencia   | Comentario                   |
|----------------|----------------------------------------------|------------|------------------------------|
| Docker         | Contenedores para entorno y despliegue       | Apache 2.0 | Portabilidad entre entornos. |
| Docker Compose | Orquestación de servicios (API + DB + Redis) | Apache 2.0 | Ideal para desarrollo local. |