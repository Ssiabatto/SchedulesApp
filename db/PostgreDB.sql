-- Base de datos: Sistema de Gestión de Turnos para Vigilantes
-- Crear la base de datos con codificación UTF8 y configuración regional en español
CREATE DATABASE gestion_turnos_vigilantes
    WITH ENCODING 'UTF8' -- Codificación de caracteres
    LC_COLLATE = 'es_ES.UTF-8' -- Configuración regional para ordenación
    LC_CTYPE = 'es_ES.UTF-8' -- Configuración regional para clasificación de caracteres
    TEMPLATE template0; -- Usar un template limpio para la base de datos

-- Usar la base de datos creada
\c gestion_turnos_vigilantes;

-- Tabla de Usuarios del Sistema
-- Esta tabla almacena la información de los usuarios que acceden al sistema
CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada usuario
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE, -- Nombre de usuario único
    password TEXT NOT NULL, -- Contraseña (almacenada como hash bcrypt)
    rol VARCHAR(50) CHECK (rol IN ('operador_supervisor', 'auxiliar_administrativo')) NOT NULL, -- Rol del usuario con valores restringidos
    nombre_completo VARCHAR(100) NOT NULL, -- Nombre completo del usuario
    email VARCHAR(100) NOT NULL, -- Correo electrónico del usuario
    activo BOOLEAN DEFAULT TRUE, -- Indica si el usuario está activo (por defecto, TRUE)
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación del usuario (por defecto, la fecha actual)
    ultima_sesion TIMESTAMP -- Fecha y hora de la última sesión del usuario
);

-- Trigger para validar el máximo de usuarios por rol
-- Esta función asegura que no haya más de 5 usuarios activos por rol
CREATE OR REPLACE FUNCTION validar_max_usuarios_por_rol()
RETURNS TRIGGER AS $$
BEGIN
    -- Contar los usuarios activos con el mismo rol que el nuevo registro
    IF (SELECT COUNT(*) FROM usuarios WHERE rol = NEW.rol AND activo = TRUE) >= 5 THEN
        -- Si ya hay 5 usuarios activos con ese rol, lanzar un error
        RAISE EXCEPTION 'No se pueden tener más de 5 usuarios activos con el rol %', NEW.rol;
    END IF;
    -- Si no se supera el límite, permitir la operación
    RETURN NEW;
END;
$$ LANGUAGE plpgsql; -- Especificar que la función está escrita en PL/pgSQL

-- Crear el trigger para ejecutar la función antes de insertar o actualizar un usuario
CREATE TRIGGER trg_validar_max_usuarios_por_rol
BEFORE INSERT OR UPDATE ON usuarios -- El trigger se ejecuta antes de insertar o actualizar un registro en la tabla "usuarios"
FOR EACH ROW -- Se ejecuta para cada fila afectada
WHEN (NEW.activo = TRUE) -- Solo se ejecuta si el nuevo registro tiene el campo "activo" en TRUE
EXECUTE FUNCTION validar_max_usuarios_por_rol(); -- Llama a la función que valida el límite de usuarios por rol

-- Tabla de Vigilantes
-- Esta tabla almacena la información de los vigilantes registrados en el sistema
CREATE TABLE vigilantes (
    id_vigilante SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada vigilante
    nombre_completo VARCHAR(100) NOT NULL, -- Nombre completo del vigilante
    numero_identificacion VARCHAR(20) NOT NULL UNIQUE, -- Número de identificación único del vigilante
    fecha_nacimiento DATE NOT NULL, -- Fecha de nacimiento del vigilante
    telefono_celular VARCHAR(20) NOT NULL, -- Número de teléfono celular del vigilante
    correo_electronico VARCHAR(100), -- Correo electrónico del vigilante (opcional)
    direccion_calle INT NOT NULL, -- Número de la calle de la dirección del vigilante
    direccion_carrera INT NOT NULL, -- Número de la carrera de la dirección del vigilante
    direccion_completa VARCHAR(255) NOT NULL, -- Dirección completa del vigilante
    contacto_emergencia_nombre VARCHAR(100) NOT NULL, -- Nombre del contacto de emergencia
    contacto_emergencia_telefono VARCHAR(20) NOT NULL, -- Teléfono del contacto de emergencia
    tipo_contrato VARCHAR(50) CHECK (tipo_contrato IN ('fijo_full_time', 'relevo_part_time')) NOT NULL, -- Tipo de contrato del vigilante
    edificios VARCHAR(50) NOT NULL, -- Edificios asignados al vigilante (ajustar según el contexto)
    salario NUMERIC(10, 2) NOT NULL, -- Salario del vigilante
    fecha_contratacion DATE NOT NULL, -- Fecha de contratación del vigilante
    foto BYTEA, -- Foto del vigilante almacenada como binario
    activo BOOLEAN DEFAULT TRUE -- Indica si el vigilante está activo (por defecto, TRUE)
);

-- Tabla de Certificaciones de Vigilantes
-- Esta tabla almacena las certificaciones de los vigilantes registrados en el sistema
CREATE TABLE certificaciones_vigilantes (
    id_certificacion SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada certificación
    id_vigilante INT NOT NULL, -- Identificador del vigilante al que pertenece la certificación
    curso_vigilancia BOOLEAN DEFAULT FALSE, -- Indica si el vigilante tiene el curso de vigilancia (por defecto, FALSE)
    manejo_armas BOOLEAN DEFAULT FALSE, -- Indica si el vigilante tiene certificación en manejo de armas (por defecto, FALSE)
    medios_electronicos BOOLEAN DEFAULT FALSE, -- Indica si el vigilante tiene certificación en medios electrónicos (por defecto, FALSE)
    primeros_auxilios BOOLEAN DEFAULT FALSE, -- Indica si el vigilante tiene certificación en primeros auxilios (por defecto, FALSE)
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de la última actualización de la certificación
    CONSTRAINT fk_vigilante FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante) ON DELETE CASCADE -- Relación con la tabla "vigilantes", elimina las certificaciones si el vigilante es eliminado
);

-- Tabla de Edificios
-- Esta tabla almacena la información de los edificios donde trabajan los vigilantes
CREATE TABLE edificios (
    id_edificio SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada edificio
    nombre VARCHAR(100) NOT NULL, -- Nombre del edificio
    direccion_calle INT NOT NULL, -- Número de la calle de la dirección del edificio
    direccion_carrera INT NOT NULL, -- Número de la carrera de la dirección del edificio
    direccion_completa VARCHAR(255) NOT NULL, -- Dirección completa del edificio
    telefono VARCHAR(20), -- Teléfono de contacto del edificio (opcional)
    administrador VARCHAR(100), -- Nombre del administrador del edificio (opcional)
    telefono_administrador VARCHAR(20), -- Teléfono del administrador del edificio (opcional)
    tipo_turno VARCHAR(20) CHECK (tipo_turno IN ('8_horas', '12_horas', '24_horas')) NOT NULL, -- Tipo de turno asignado al edificio
    horas_semanales INT NOT NULL CHECK (horas_semanales >= 40 AND horas_semanales <= 48), -- Horas semanales permitidas (entre 40 y 48)
    activo BOOLEAN DEFAULT TRUE -- Indica si el edificio está activo (por defecto, TRUE)
);

-- Tabla de Tipos de Turnos
-- Esta tabla almacena los diferentes tipos de turnos disponibles en el sistema
CREATE TABLE tipos_turnos (
    id_tipo_turno SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada tipo de turno
    nombre VARCHAR(50) NOT NULL, -- Nombre del tipo de turno
    hora_inicio TIME NOT NULL, -- Hora de inicio del turno
    hora_fin TIME NOT NULL, -- Hora de finalización del turno
    duracion INT NOT NULL, -- Duración del turno en horas
    descripcion VARCHAR(255) -- Descripción adicional del turno (opcional)
);

-- Definición de turnos estándar
-- Inserta los turnos predefinidos en la tabla "tipos_turnos"
INSERT INTO tipos_turnos (nombre, hora_inicio, hora_fin, duracion, descripcion) VALUES
('Diurno 8h A', '06:00:00', '14:00:00', 8, 'Turno diurno de 8 horas (6-14)'),
('Diurno 8h B', '14:00:00', '22:00:00', 8, 'Turno tarde de 8 horas (14-22)'),
('Nocturno 8h', '22:00:00', '06:00:00', 8, 'Turno nocturno de 8 horas (22-6)'),
('Diurno 12h', '07:00:00', '19:00:00', 12, 'Turno diurno de 12 horas (7-19)'),
('Nocturno 12h', '19:00:00', '07:00:00', 12, 'Turno nocturno de 12 horas (19-7)'),
('24h Día', '07:00:00', '07:00:00', 24, 'Turno completo de 24 horas (7-7)'),
('24h Noche', '19:00:00', '19:00:00', 24, 'Turno completo de 24 horas (19-19)');

-- Tabla de Configuración del Sistema
-- Esta tabla almacena la configuración general del sistema
CREATE TABLE configuracion_sistema (
    id_configuracion SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada configuración
    minimo_horas_descanso INT NOT NULL DEFAULT 8 CHECK (minimo_horas_descanso >= 1 AND minimo_horas_descanso <= 12), -- Mínimo de horas de descanso permitido (entre 1 y 12)
    ultimo_backup DATE, -- Fecha del último respaldo realizado
    ultima_limpieza_trimestral DATE, -- Fecha de la última limpieza trimestral
    actualizado_por INT, -- Identificador del usuario que realizó la última actualización
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de la última actualización (por defecto, la fecha actual)
    CONSTRAINT fk_actualizado_por FOREIGN KEY (actualizado_por) REFERENCES usuarios(id_usuario) -- Relación con la tabla "usuarios"
);

-- Tabla de Planificación de Turnos (planilla mensual)
-- Esta tabla almacena la planificación mensual de turnos
CREATE TABLE planilla_turnos (
    id_planilla SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada planilla
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12), -- Mes de la planilla (entre 1 y 12)
    anio INT NOT NULL, -- Año de la planilla
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de generación de la planilla (por defecto, la fecha actual)
    generado_por INT, -- Identificador del usuario que generó la planilla
    estado VARCHAR(20) CHECK (estado IN ('borrador', 'publicado', 'archivado')) DEFAULT 'borrador', -- Estado de la planilla (borrador, publicado o archivado)
    CONSTRAINT fk_generado_por FOREIGN KEY (generado_por) REFERENCES usuarios(id_usuario), -- Relación con la tabla "usuarios"
    UNIQUE (mes, anio) -- Restricción para que no existan duplicados de planillas en el mismo mes y año
);

-- Tabla de Asignación de Turnos
-- Esta tabla almacena la asignación de turnos a los vigilantes
CREATE TABLE asignaciones_turnos (
    id_asignacion SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada asignación
    id_planilla INT NOT NULL, -- Identificador de la planilla a la que pertenece la asignación
    id_vigilante INT NOT NULL, -- Identificador del vigilante asignado al turno
    id_edificio INT NOT NULL, -- Identificador del edificio donde se realiza el turno
    id_tipo_turno INT NOT NULL, -- Identificador del tipo de turno asignado
    fecha DATE NOT NULL, -- Fecha del turno
    hora_inicio TIMESTAMP NOT NULL, -- Hora de inicio del turno
    hora_fin TIMESTAMP NOT NULL, -- Hora de finalización del turno
    es_turno_habitual BOOLEAN DEFAULT TRUE, -- Indica si el turno es habitual (por defecto, TRUE)
    estado VARCHAR(20) CHECK (estado IN ('programado', 'confirmado', 'completado', 'ausente')) DEFAULT 'programado', -- Estado del turno
    creado_por INT, -- Identificador del usuario que creó la asignación
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la asignación (por defecto, la fecha actual)
    CONSTRAINT fk_planilla FOREIGN KEY (id_planilla) REFERENCES planilla_turnos(id_planilla), -- Relación con la tabla "planilla_turnos"
    CONSTRAINT fk_vigilante FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante), -- Relación con la tabla "vigilantes"
    CONSTRAINT fk_edificio FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio), -- Relación con la tabla "edificios"
    CONSTRAINT fk_tipo_turno FOREIGN KEY (id_tipo_turno) REFERENCES tipos_turnos(id_tipo_turno), -- Relación con la tabla "tipos_turnos"
    CONSTRAINT fk_creado_por FOREIGN KEY (creado_por) REFERENCES usuarios(id_usuario) -- Relación con la tabla "usuarios"
);

-- Tabla de Novedades y Contingencias
-- Esta tabla almacena las novedades y contingencias relacionadas con los turnos
CREATE TABLE novedades (
    id_novedad SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada novedad
    id_asignacion_original INT, -- Identificador de la asignación original afectada por la novedad
    id_vigilante_original INT NOT NULL, -- Identificador del vigilante afectado por la novedad
    id_vigilante_reemplazo INT, -- Identificador del vigilante que reemplaza al original (opcional)
    id_edificio INT NOT NULL, -- Identificador del edificio donde ocurre la novedad
    fecha_novedad DATE NOT NULL, -- Fecha de la novedad
    hora_inicio TIMESTAMP NOT NULL, -- Hora de inicio de la novedad
    hora_fin TIMESTAMP NOT NULL, -- Hora de finalización de la novedad
    tipo_novedad VARCHAR(50) CHECK (tipo_novedad IN ('incapacidad', 'ausencia', 'contingencia', 'despido', 'calamidad', 'permiso', 'vacaciones', 'solicitud_vigilante')) NOT NULL, -- Tipo de novedad
    descripcion TEXT, -- Descripción adicional de la novedad
    estado VARCHAR(20) CHECK (estado IN ('pendiente', 'resuelta', 'cancelada')) DEFAULT 'pendiente', -- Estado de la novedad
    registrado_por INT, -- Identificador del usuario que registró la novedad
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de registro de la novedad (por defecto, la fecha actual)
    CONSTRAINT fk_asignacion_original FOREIGN KEY (id_asignacion_original) REFERENCES asignaciones_turnos(id_asignacion), -- Relación con la tabla "asignaciones_turnos"
    CONSTRAINT fk_vigilante_original FOREIGN KEY (id_vigilante_original) REFERENCES vigilantes(id_vigilante), -- Relación con la tabla "vigilantes"
    CONSTRAINT fk_vigilante_reemplazo FOREIGN KEY (id_vigilante_reemplazo) REFERENCES vigilantes(id_vigilante), -- Relación con la tabla "vigilantes"
    CONSTRAINT fk_edificio FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio), -- Relación con la tabla "edificios"
    CONSTRAINT fk_registrado_por FOREIGN KEY (registrado_por) REFERENCES usuarios(id_usuario) -- Relación con la tabla "usuarios"
);

-- Tabla de Registro de Horas Trabajadas
-- Esta tabla almacena el registro de las horas trabajadas por los vigilantes
CREATE TABLE registro_horas (
    id_registro SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada registro
    id_asignacion INT NOT NULL, -- Identificador de la asignación de turno
    id_vigilante INT NOT NULL, -- Identificador del vigilante
    id_edificio INT NOT NULL, -- Identificador del edificio donde se trabajó
    fecha DATE NOT NULL, -- Fecha del registro
    hora_inicio TIMESTAMP NOT NULL, -- Hora de inicio del trabajo
    hora_fin TIMESTAMP NOT NULL, -- Hora de finalización del trabajo
    horas_normales NUMERIC(5,2) DEFAULT 0, -- Horas normales trabajadas
    horas_extras_diurnas NUMERIC(5,2) DEFAULT 0, -- Horas extras diurnas trabajadas
    horas_extras_nocturnas NUMERIC(5,2) DEFAULT 0, -- Horas extras nocturnas trabajadas
    horas_extras_festivas_diurnas NUMERIC(5,2) DEFAULT 0, -- Horas extras festivas diurnas trabajadas
    horas_extras_festivas_nocturnas NUMERIC(5,2) DEFAULT 0, -- Horas extras festivas nocturnas trabajadas
    es_festivo BOOLEAN DEFAULT FALSE, -- Indica si el día es festivo (por defecto, FALSE)
    calculado_por INT, -- Identificador del usuario que realizó el cálculo
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha en que se realizó el cálculo (por defecto, la fecha actual)
    CONSTRAINT fk_asignacion FOREIGN KEY (id_asignacion) REFERENCES asignaciones_turnos(id_asignacion), -- Relación con la tabla "asignaciones_turnos"
    CONSTRAINT fk_vigilante FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante), -- Relación con la tabla "vigilantes"
    CONSTRAINT fk_edificio FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio), -- Relación con la tabla "edificios"
    CONSTRAINT fk_calculado_por FOREIGN KEY (calculado_por) REFERENCES usuarios(id_usuario) -- Relación con la tabla "usuarios"
);

-- Tabla para Fechas Festivas en Colombia
-- Esta tabla almacena las fechas festivas en Colombia
CREATE TABLE festivos_colombia (
    id_festivo SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada fecha festiva
    fecha DATE NOT NULL UNIQUE, -- Fecha festiva (única)
    descripcion VARCHAR(100), -- Descripción de la festividad (opcional)
    anio INT GENERATED ALWAYS AS (EXTRACT(YEAR FROM fecha)) STORED -- Año de la festividad (generado automáticamente a partir de la fecha)
);

-- Tabla de Liquidación Mensual
-- Esta tabla almacena la liquidación mensual de horas y valores para cada vigilante
CREATE TABLE liquidacion_mensual (
    id_liquidacion SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada liquidación
    id_vigilante INT NOT NULL, -- Identificador del vigilante
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12), -- Mes de la liquidación (entre 1 y 12)
    anio INT NOT NULL, -- Año de la liquidación
    total_horas_normales NUMERIC(6,2) DEFAULT 0, -- Total de horas normales trabajadas
    total_horas_extras_diurnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras diurnas trabajadas
    total_horas_extras_nocturnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras nocturnas trabajadas
    total_horas_extras_festivas_diurnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras festivas diurnas trabajadas
    total_horas_extras_festivas_nocturnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras festivas nocturnas trabajadas
    valor_horas_normales NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas normales
    valor_horas_extras_diurnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras diurnas
    valor_horas_extras_nocturnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras nocturnas
    valor_horas_extras_festivas_diurnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras festivas diurnas
    valor_horas_extras_festivas_nocturnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras festivas nocturnas
    valor_total NUMERIC(12,2) DEFAULT 0, -- Valor total de la liquidación
    procesado_por INT, -- Identificador del usuario que procesó la liquidación
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de procesamiento de la liquidación (por defecto, la fecha actual)
    CONSTRAINT fk_vigilante FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante), -- Relación con la tabla "vigilantes"
    CONSTRAINT fk_procesado_por FOREIGN KEY (procesado_por) REFERENCES usuarios(id_usuario), -- Relación con la tabla "usuarios"
    UNIQUE (id_vigilante, mes, anio) -- Restricción para evitar duplicados de liquidaciones para el mismo vigilante, mes y año
);

-- Tabla de Liquidación por Edificio
-- Esta tabla almacena la liquidación mensual de horas y valores para cada edificio
CREATE TABLE liquidacion_edificio (
    id_liquidacion_edificio SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada liquidación
    id_edificio INT NOT NULL, -- Identificador del edificio
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12), -- Mes de la liquidación (entre 1 y 12)
    anio INT NOT NULL, -- Año de la liquidación
    total_horas_normales NUMERIC(6,2) DEFAULT 0, -- Total de horas normales trabajadas en el edificio
    total_horas_extras_diurnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras diurnas trabajadas en el edificio
    total_horas_extras_nocturnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras nocturnas trabajadas en el edificio
    total_horas_extras_festivas_diurnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras festivas diurnas trabajadas en el edificio
    total_horas_extras_festivas_nocturnas NUMERIC(6,2) DEFAULT 0, -- Total de horas extras festivas nocturnas trabajadas en el edificio
    valor_horas_normales NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas normales en el edificio
    valor_horas_extras_diurnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras diurnas en el edificio
    valor_horas_extras_nocturnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras nocturnas en el edificio
    valor_horas_extras_festivas_diurnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras festivas diurnas en el edificio
    valor_horas_extras_festivas_nocturnas NUMERIC(10,2) DEFAULT 0, -- Valor total de las horas extras festivas nocturnas en el edificio
    valor_total NUMERIC(12,2) DEFAULT 0, -- Valor total de la liquidación del edificio
    procesado_por INT, -- Identificador del usuario que procesó la liquidación
    fecha_procesamiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de procesamiento de la liquidación (por defecto, la fecha actual)
    CONSTRAINT fk_edificio FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio), -- Relación con la tabla "edificios"
    CONSTRAINT fk_procesado_por FOREIGN KEY (procesado_por) REFERENCES usuarios(id_usuario), -- Relación con la tabla "usuarios"
    UNIQUE (id_edificio, mes, anio) -- Restricción para evitar duplicados de liquidaciones para el mismo edificio, mes y año
);

-- Tabla de Registro de Sesiones (para control de concurrencia)
-- Esta tabla almacena las sesiones activas de los usuarios
CREATE TABLE sesiones_activas (
    id_sesion SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada sesión
    id_usuario INT NOT NULL, -- Identificador del usuario asociado a la sesión
    token VARCHAR(255) NOT NULL, -- Token único de la sesión
    ip_address VARCHAR(45) NOT NULL, -- Dirección IP del usuario
    inicio_sesion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de inicio de la sesión
    ultimo_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora del último acceso
    estado VARCHAR(20) CHECK (estado IN ('activa', 'cerrada')) DEFAULT 'activa', -- Estado de la sesión (activa o cerrada)
    CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) -- Relación con la tabla "usuarios"
);

-- Tabla de Backups
-- Esta tabla almacena el registro de los backups realizados en el sistema
CREATE TABLE registro_backups (
    id_backup SERIAL PRIMARY KEY, -- Identificador único autoincremental para cada backup
    nombre_archivo VARCHAR(255) NOT NULL, -- Nombre del archivo de backup
    fecha_backup TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora en que se realizó el backup
    trimestre INT NOT NULL CHECK (trimestre >= 1 AND trimestre <= 4), -- Trimestre en el que se realizó el backup (entre 1 y 4)
    anio INT NOT NULL, -- Año en el que se realizó el backup
    tamanio_bytes BIGINT, -- Tamaño del archivo de backup en bytes
    realizado_por INT, -- Identificador del usuario que realizó el backup
    estado VARCHAR(20) CHECK (estado IN ('generado', 'descargado', 'eliminado')) DEFAULT 'generado', -- Estado del backup (generado, descargado o eliminado)
    fecha_eliminacion TIMESTAMP, -- Fecha y hora en que se eliminó el backup (opcional)
    CONSTRAINT fk_realizado_por FOREIGN KEY (realizado_por) REFERENCES usuarios(id_usuario) -- Relación con la tabla "usuarios"
);

-- Procedimiento almacenado para verificar y validar la concurrencia de sesiones
-- Este procedimiento valida que no haya más de una sesión activa para operadores supervisores
CREATE OR REPLACE FUNCTION validar_sesion_operador(p_id_usuario INT, p_token VARCHAR(255))
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    v_rol VARCHAR(50);
    v_count INT;
BEGIN
    -- Obtener el rol del usuario
    SELECT rol INTO v_rol FROM usuarios WHERE id_usuario = p_id_usuario;

    -- Si es operador_supervisor, verificar si ya hay otra sesión activa
    IF v_rol = 'operador_supervisor' THEN
        SELECT COUNT(*) INTO v_count
        FROM sesiones_activas
        WHERE estado = 'activa' AND id_usuario != p_id_usuario AND 
              id_usuario IN (SELECT id_usuario FROM usuarios WHERE rol = 'operador_supervisor');

        -- Si ya hay una sesión activa, lanzar un error
        IF v_count > 0 THEN
            RAISE EXCEPTION 'Ya existe una sesión activa de operador supervisor.';
        END IF;
    END IF;

    -- Actualizar o crear la sesión del usuario actual
    UPDATE sesiones_activas
    SET ultimo_acceso = CURRENT_TIMESTAMP
    WHERE id_usuario = p_id_usuario AND token = p_token;
END;
$$;

-- Función para calcular distancia entre direcciones (simple aproximación cartesiana)
-- Esta función calcula la distancia entre dos puntos dados por calle y carrera
CREATE OR REPLACE FUNCTION calcular_distancia(calle1 INT, carrera1 INT, calle2 INT, carrera2 INT)
RETURNS NUMERIC(10,2) LANGUAGE plpgsql AS $$
DECLARE
    distancia NUMERIC(10,2);
BEGIN
    -- Calcular la distancia usando la fórmula de distancia euclidiana
    distancia := SQRT(POWER(calle2 - calle1, 2) + POWER(carrera2 - carrera1, 2));
    RETURN distancia;
END;
$$;

-- Procedimiento almacenado para encontrar vigilantes disponibles para contingencias
-- Este procedimiento busca vigilantes disponibles para un turno específico, considerando descansos mínimos y proximidad al edificio
CREATE OR REPLACE FUNCTION encontrar_vigilantes_disponibles(
    p_fecha DATE,
    p_hora_inicio TIME,
    p_hora_fin TIME,
    p_id_edificio INT,
    p_horas_minimas_descanso INT
)
RETURNS TABLE (
    id_vigilante INT,
    nombre_completo VARCHAR(100),
    tipo_contrato VARCHAR(50),
    distancia NUMERIC(10,2),
    horas_desde_ultimo_turno INT,
    horas_hasta_siguiente_turno INT
) LANGUAGE plpgsql AS $$
DECLARE
    v_calle_edificio INT;
    v_carrera_edificio INT;
BEGIN
    -- Obtener coordenadas del edificio
    SELECT direccion_calle, direccion_carrera INTO v_calle_edificio, v_carrera_edificio
    FROM edificios WHERE id_edificio = p_id_edificio;

    -- Retornar vigilantes disponibles
    RETURN QUERY
    SELECT 
        v.id_vigilante,
        v.nombre_completo,
        v.tipo_contrato,
        calcular_distancia(v.direccion_calle, v.direccion_carrera, v_calle_edificio, v_carrera_edificio) AS distancia,
        EXTRACT(EPOCH FROM (
            (SELECT MAX(a.hora_fin) 
             FROM asignaciones_turnos a
             WHERE a.id_vigilante = v.id_vigilante 
               AND a.fecha = p_fecha 
               AND a.hora_fin <= (p_fecha || ' ' || p_hora_inicio)::TIMESTAMP
            ) - (p_fecha || ' ' || p_hora_inicio)::TIMESTAMP
        )) / 3600 AS horas_desde_ultimo_turno,
        EXTRACT(EPOCH FROM (
            (p_fecha || ' ' || p_hora_fin)::TIMESTAMP - 
            (SELECT MIN(a.hora_inicio) 
             FROM asignaciones_turnos a
             WHERE a.id_vigilante = v.id_vigilante 
               AND a.fecha >= p_fecha 
               AND a.hora_inicio >= (p_fecha || ' ' || p_hora_fin)::TIMESTAMP
            )
        )) / 3600 AS horas_hasta_siguiente_turno
    FROM 
        vigilantes v
    LEFT JOIN 
        asignaciones_turnos a ON v.id_vigilante = a.id_vigilante 
            AND ((p_fecha || ' ' || p_hora_inicio)::TIMESTAMP BETWEEN a.hora_inicio AND a.hora_fin 
              OR (p_fecha || ' ' || p_hora_fin)::TIMESTAMP BETWEEN a.hora_inicio AND a.hora_fin
              OR a.hora_inicio BETWEEN (p_fecha || ' ' || p_hora_inicio)::TIMESTAMP AND (p_fecha || ' ' || p_hora_fin)::TIMESTAMP)
    WHERE 
        v.activo = TRUE
        AND a.id_asignacion IS NULL
    GROUP BY 
        v.id_vigilante, v.nombre_completo, v.tipo_contrato, v.direccion_calle, v.direccion_carrera
    HAVING 
        (horas_desde_ultimo_turno IS NULL OR horas_desde_ultimo_turno >= p_horas_minimas_descanso)
        AND (horas_hasta_siguiente_turno IS NULL OR horas_hasta_siguiente_turno >= p_horas_minimas_descanso)
    ORDER BY 
        -- Priorizar vigilantes part-time, luego por distancia
        CASE WHEN v.tipo_contrato = 'relevo_part_time' THEN 0 ELSE 1 END,
        distancia ASC;
END;
$$;

-- Procedimiento almacenado para calcular horas extras
-- Este procedimiento calcula las horas normales y extras de una asignación específica
CREATE OR REPLACE FUNCTION calcular_horas_extras(p_id_asignacion INT)
RETURNS VOID LANGUAGE plpgsql AS $$
DECLARE
    v_hora_inicio TIMESTAMP;
    v_hora_fin TIMESTAMP;
    v_fecha DATE;
    v_id_vigilante INT;
    v_id_edificio INT;
    v_es_festivo BOOLEAN DEFAULT FALSE;
    v_horas_normales NUMERIC(5,2) DEFAULT 0;
    v_horas_extras_diurnas NUMERIC(5,2) DEFAULT 0;
    v_horas_extras_nocturnas NUMERIC(5,2) DEFAULT 0;
    v_horas_extras_festivas_diurnas NUMERIC(5,2) DEFAULT 0;
    v_horas_extras_festivas_nocturnas NUMERIC(5,2) DEFAULT 0;
BEGIN
    -- Obtener datos del turno
    SELECT 
        hora_inicio, 
        hora_fin, 
        DATE(hora_inicio), 
        id_vigilante, 
        id_edificio
    INTO 
        v_hora_inicio, 
        v_hora_fin, 
        v_fecha, 
        v_id_vigilante, 
        v_id_edificio
    FROM 
        asignaciones_turnos 
    WHERE 
        id_asignacion = p_id_asignacion;

    -- Verificar si es festivo
    SELECT EXISTS (
        SELECT 1 
        FROM festivos_colombia 
        WHERE fecha = v_fecha
    ) INTO v_es_festivo;

    -- Lógica para calcular horas normales y extras
    IF v_es_festivo THEN
        -- En festivos, todas las horas son extras festivas
        v_horas_extras_festivas_diurnas := EXTRACT(EPOCH FROM (v_hora_fin - v_hora_inicio)) / 3600;
    ELSE
        -- En días normales, calcular según horario
        -- Esta es una simplificación, la lógica real sería más compleja
        v_horas_normales := EXTRACT(EPOCH FROM (v_hora_fin - v_hora_inicio)) / 3600;
    END IF;

    -- Insertar o actualizar el registro de horas
    INSERT INTO registro_horas (
        id_asignacion,
        id_vigilante,
        id_edificio,
        fecha,
        hora_inicio,
        hora_fin,
        horas_normales,
        horas_extras_diurnas,
        horas_extras_nocturnas,
        horas_extras_festivas_diurnas,
        horas_extras_festivas_nocturnas,
        es_festivo
    ) VALUES (
        p_id_asignacion,
        v_id_vigilante,
        v_id_edificio,
        v_fecha,
        v_hora_inicio,
        v_hora_fin,
        v_horas_normales,
        v_horas_extras_diurnas,
        v_horas_extras_nocturnas,
        v_horas_extras_festivas_diurnas,
        v_horas_extras_festivas_nocturnas,
        v_es_festivo
    )
    ON CONFLICT (id_asignacion) DO UPDATE
    SET 
        horas_normales = EXCLUDED.horas_normales,
        horas_extras_diurnas = EXCLUDED.horas_extras_diurnas,
        horas_extras_nocturnas = EXCLUDED.horas_extras_nocturnas,
        horas_extras_festivas_diurnas = EXCLUDED.horas_extras_festivas_diurnas,
        horas_extras_festivas_nocturnas = EXCLUDED.horas_extras_festivas_nocturnas,
        es_festivo = EXCLUDED.es_festivo,
        fecha_calculo = CURRENT_TIMESTAMP;
END;
$$;

-- Trigger para calcular horas extras al completar un turno
-- Este trigger llama a la función `calcular_horas_extras` cuando un turno cambia a estado "completado"
CREATE OR REPLACE FUNCTION after_asignacion_completada()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado = 'completado' AND OLD.estado != 'completado' THEN
        PERFORM calcular_horas_extras(NEW.id_asignacion);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_after_asignacion_completada
AFTER UPDATE ON asignaciones_turnos
FOR EACH ROW
EXECUTE FUNCTION after_asignacion_completada();

-- Vista para ver vigilantes disponibles en un momento dado
-- Esta vista muestra los vigilantes disponibles con información sobre su último y próximo turno
CREATE OR REPLACE VIEW vista_vigilantes_disponibles AS
SELECT 
    v.id_vigilante,
    v.nombre_completo,
    v.tipo_contrato,
    v.telefono_celular,
    MAX(a.hora_fin) AS ultimo_turno_fin,
    MIN(CASE WHEN a.hora_inicio > CURRENT_TIMESTAMP THEN a.hora_inicio ELSE NULL END) AS proximo_turno_inicio
FROM 
    vigilantes v
LEFT JOIN 
    asignaciones_turnos a ON v.id_vigilante = a.id_vigilante AND 
    (a.hora_fin < CURRENT_TIMESTAMP OR a.hora_inicio > CURRENT_TIMESTAMP)
WHERE 
    v.activo = TRUE
GROUP BY 
    v.id_vigilante;

-- Vista para el dashboard de cobertura de edificios
-- Esta vista muestra la cobertura de edificios en los próximos 7 días
CREATE OR REPLACE VIEW vista_cobertura_edificios AS
SELECT 
    e.id_edificio,
    e.nombre AS edificio,
    DATE(a.fecha) AS fecha,
    EXTRACT(HOUR FROM a.hora_inicio) AS hora,
    COUNT(DISTINCT a.id_vigilante) AS vigilantes_asignados
FROM 
    edificios e
LEFT JOIN 
    asignaciones_turnos a ON e.id_edificio = a.id_edificio
WHERE 
    a.fecha BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
GROUP BY 
    e.id_edificio, DATE(a.fecha), EXTRACT(HOUR FROM a.hora_inicio);

-- Creación de usuario administrador por defecto (password: admin123 en MD5)
-- Nota: PostgreSQL no tiene una función MD5 integrada en SQL puro, pero se puede usar `md5()` en plpgsql
INSERT INTO usuarios (nombre_usuario, password, rol, nombre_completo, email) 
VALUES ('admin', md5('admin123'), 'operador_supervisor', 'Administrador Sistema', 'admin@example.com');

-- Configuración inicial del sistema
-- Inserta la configuración inicial con un mínimo de horas de descanso
INSERT INTO configuracion_sistema (minimo_horas_descanso, actualizado_por) 
VALUES (8, 1);