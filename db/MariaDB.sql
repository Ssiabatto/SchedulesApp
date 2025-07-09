-- Base de datos: Sistema de Gestión de Turnos para Vigilantes
CREATE DATABASE IF NOT EXISTS gestion_turnos_vigilantes CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE gestion_turnos_vigilantes;

-- Tabla de Usuarios del Sistema
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, -- Para almacenar hash MD5
    rol ENUM('operador_supervisor', 'auxiliar_administrativo') NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultima_sesion DATETIME,
    CONSTRAINT chk_max_usuarios CHECK ((SELECT COUNT(*) FROM usuarios WHERE rol = 'operador_supervisor') <= 5 AND 
                                      (SELECT COUNT(*) FROM usuarios WHERE rol = 'auxiliar_administrativo') <= 5)
);

-- Tabla de Vigilantes
CREATE TABLE vigilantes (
    id_vigilante INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    numero_identificacion VARCHAR(20) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    telefono_celular VARCHAR(20) NOT NULL,
    correo_electronico VARCHAR(100),
    direccion_calle INT NOT NULL,
    direccion_carrera INT NOT NULL,
    direccion_completa VARCHAR(255) NOT NULL,
    contacto_emergencia_nombre VARCHAR(100) NOT NULL,
    contacto_emergencia_telefono VARCHAR(20) NOT NULL,
    tipo_contrato ENUM('fijo_full_time', 'relevo_part_time') NOT NULL,
    edificios ENUM('edificios') NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    foto MEDIUMBLOB,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Certificaciones de Vigilantes
CREATE TABLE certificaciones_vigilantes (
    id_certificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_vigilante INT NOT NULL,
    curso_vigilancia BOOLEAN DEFAULT FALSE,
    manejo_armas BOOLEAN DEFAULT FALSE,
    medios_electronicos BOOLEAN DEFAULT FALSE,
    primeros_auxilios BOOLEAN DEFAULT FALSE,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante) ON DELETE CASCADE
);

-- Tabla de Edificios
CREATE TABLE edificios (
    id_edificio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion_calle INT NOT NULL,
    direccion_carrera INT NOT NULL,
    direccion_completa VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    administrador VARCHAR(100),
    telefono_administrador VARCHAR(20),
    tipo_turno ENUM('8_horas', '12_horas', '24_horas') NOT NULL,
    horas_semanales INT NOT NULL CHECK (horas_semanales >= 40 AND horas_semanales <= 48),
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Tipos de Turnos
CREATE TABLE tipos_turnos (
    id_tipo_turno INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    duracion INT NOT NULL, -- Duración en horas
    descripcion VARCHAR(255)
);

-- Definición de turnos estándar
INSERT INTO tipos_turnos (nombre, hora_inicio, hora_fin, duracion, descripcion) VALUES
('Diurno 8h A', '06:00:00', '14:00:00', 8, 'Turno diurno de 8 horas (6-14)'),
('Diurno 8h B', '14:00:00', '22:00:00', 8, 'Turno tarde de 8 horas (14-22)'),
('Nocturno 8h', '22:00:00', '06:00:00', 8, 'Turno nocturno de 8 horas (22-6)'),
('Diurno 12h', '07:00:00', '19:00:00', 12, 'Turno diurno de 12 horas (7-19)'),
('Nocturno 12h', '19:00:00', '07:00:00', 12, 'Turno nocturno de 12 horas (19-7)'),
('24h Día', '07:00:00', '07:00:00', 24, 'Turno completo de 24 horas (7-7)'),
('24h Noche', '19:00:00', '19:00:00', 24, 'Turno completo de 24 horas (19-19)');

-- Tabla de Configuración del Sistema
CREATE TABLE configuracion_sistema (
    id_configuracion INT AUTO_INCREMENT PRIMARY KEY,
    minimo_horas_descanso INT NOT NULL DEFAULT 8 CHECK (minimo_horas_descanso >= 1 AND minimo_horas_descanso <= 12),
    ultimo_backup DATE,
    ultima_limpieza_trimestral DATE,
    actualizado_por INT,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (actualizado_por) REFERENCES usuarios(id_usuario)
);

-- Tabla de Planificación de Turnos (planilla mensual)
CREATE TABLE planilla_turnos (
    id_planilla INT AUTO_INCREMENT PRIMARY KEY,
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12),
    anio INT NOT NULL,
    fecha_generacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    generado_por INT,
    estado ENUM('borrador', 'publicado', 'archivado') DEFAULT 'borrador',
    FOREIGN KEY (generado_por) REFERENCES usuarios(id_usuario),
    UNIQUE(mes, anio)
);

-- Tabla de Asignación de Turnos
CREATE TABLE asignaciones_turnos (
    id_asignacion INT AUTO_INCREMENT PRIMARY KEY,
    id_planilla INT NOT NULL,
    id_vigilante INT NOT NULL,
    id_edificio INT NOT NULL,
    id_tipo_turno INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio DATETIME NOT NULL,
    hora_fin DATETIME NOT NULL,
    es_turno_habitual BOOLEAN DEFAULT TRUE,
    estado ENUM('programado', 'confirmado', 'completado', 'ausente') DEFAULT 'programado',
    creado_por INT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_planilla) REFERENCES planilla_turnos(id_planilla),
    FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante),
    FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio),
    FOREIGN KEY (id_tipo_turno) REFERENCES tipos_turnos(id_tipo_turno),
    FOREIGN KEY (creado_por) REFERENCES usuarios(id_usuario)
);

-- Tabla de Novedades y Contingencias
CREATE TABLE novedades (
    id_novedad INT AUTO_INCREMENT PRIMARY KEY,
    id_asignacion_original INT,
    id_vigilante_original INT NOT NULL,
    id_vigilante_reemplazo INT,
    id_edificio INT NOT NULL,
    fecha_novedad DATE NOT NULL,
    hora_inicio DATETIME NOT NULL,
    hora_fin DATETIME NOT NULL,
    tipo_novedad ENUM('incapacidad', 'ausencia', 'contingencia', 'despido', 'calamidad', 'permiso', 'vacaciones', 'solicitud_vigilante') NOT NULL,
    descripcion TEXT,
    estado ENUM('pendiente', 'resuelta', 'cancelada') DEFAULT 'pendiente',
    registrado_por INT,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_asignacion_original) REFERENCES asignaciones_turnos(id_asignacion),
    FOREIGN KEY (id_vigilante_original) REFERENCES vigilantes(id_vigilante),
    FOREIGN KEY (id_vigilante_reemplazo) REFERENCES vigilantes(id_vigilante),
    FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio),
    FOREIGN KEY (registrado_por) REFERENCES usuarios(id_usuario)
);

-- Tabla de Registro de Horas Trabajadas
CREATE TABLE registro_horas (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_asignacion INT NOT NULL,
    id_vigilante INT NOT NULL,
    id_edificio INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio DATETIME NOT NULL,
    hora_fin DATETIME NOT NULL,
    horas_normales DECIMAL(5,2) DEFAULT 0,
    horas_extras_diurnas DECIMAL(5,2) DEFAULT 0,
    horas_extras_nocturnas DECIMAL(5,2) DEFAULT 0,
    horas_extras_festivas_diurnas DECIMAL(5,2) DEFAULT 0,
    horas_extras_festivas_nocturnas DECIMAL(5,2) DEFAULT 0,
    es_festivo BOOLEAN DEFAULT FALSE,
    calculado_por INT,
    fecha_calculo DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_asignacion) REFERENCES asignaciones_turnos(id_asignacion),
    FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante),
    FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio),
    FOREIGN KEY (calculado_por) REFERENCES usuarios(id_usuario)
);

-- Tabla para Fechas Festivas en Colombia
CREATE TABLE festivos_colombia (
    id_festivo INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL UNIQUE,
    descripcion VARCHAR(100),
    anio INT GENERATED ALWAYS AS (YEAR(fecha)) STORED
);

-- Tabla de Liquidación Mensual
CREATE TABLE liquidacion_mensual (
    id_liquidacion INT AUTO_INCREMENT PRIMARY KEY,
    id_vigilante INT NOT NULL,
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12),
    anio INT NOT NULL,
    total_horas_normales DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_diurnas DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_nocturnas DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_festivas_diurnas DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_festivas_nocturnas DECIMAL(6,2) DEFAULT 0,
    valor_horas_normales DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_diurnas DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_nocturnas DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_festivas_diurnas DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_festivas_nocturnas DECIMAL(10,2) DEFAULT 0,
    valor_total DECIMAL(12,2) DEFAULT 0,
    procesado_por INT,
    fecha_procesamiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_vigilante) REFERENCES vigilantes(id_vigilante),
    FOREIGN KEY (procesado_por) REFERENCES usuarios(id_usuario),
    UNIQUE(id_vigilante, mes, anio)
);

-- Tabla de Liquidación por Edificio
CREATE TABLE liquidacion_edificio (
    id_liquidacion_edificio INT AUTO_INCREMENT PRIMARY KEY,
    id_edificio INT NOT NULL,
    mes INT NOT NULL CHECK (mes >= 1 AND mes <= 12),
    anio INT NOT NULL,
    total_horas_normales DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_diurnas DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_nocturnas DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_festivas_diurnas DECIMAL(6,2) DEFAULT 0,
    total_horas_extras_festivas_nocturnas DECIMAL(6,2) DEFAULT 0,
    valor_horas_normales DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_diurnas DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_nocturnas DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_festivas_diurnas DECIMAL(10,2) DEFAULT 0,
    valor_horas_extras_festivas_nocturnas DECIMAL(10,2) DEFAULT 0,
    valor_total DECIMAL(12,2) DEFAULT 0,
    procesado_por INT,
    fecha_procesamiento DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_edificio) REFERENCES edificios(id_edificio),
    FOREIGN KEY (procesado_por) REFERENCES usuarios(id_usuario),
    UNIQUE(id_edificio, mes, anio)
);

-- Tabla de Registro de Sesiones (para control de concurrencia)
CREATE TABLE sesiones_activas (
    id_sesion INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    inicio_sesion DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('activa', 'cerrada') DEFAULT 'activa',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
);

-- Tabla de Backups
CREATE TABLE registro_backups (
    id_backup INT AUTO_INCREMENT PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    fecha_backup DATETIME DEFAULT CURRENT_TIMESTAMP,
    trimestre INT NOT NULL CHECK (trimestre >= 1 AND trimestre <= 4),
    anio INT NOT NULL,
    tamanio_bytes BIGINT,
    realizado_por INT,
    estado ENUM('generado', 'descargado', 'eliminado') DEFAULT 'generado',
    fecha_eliminacion DATETIME,
    FOREIGN KEY (realizado_por) REFERENCES usuarios(id_usuario)
);

-- Procedimiento almacenado para verificar y validar la concurrencia de sesiones
DELIMITER //
CREATE PROCEDURE validar_sesion_operador(IN p_id_usuario INT, IN p_token VARCHAR(255))
BEGIN
    DECLARE v_rol VARCHAR(50);
    DECLARE v_count INT;
    
    -- Obtener el rol del usuario
    SELECT rol INTO v_rol FROM usuarios WHERE id_usuario = p_id_usuario;
    
    -- Si es operador_supervisor, verificar si ya hay otra sesión activa
    IF v_rol = 'operador_supervisor' THEN
        SELECT COUNT(*) INTO v_count 
        FROM sesiones_activas 
        WHERE estado = 'activa' AND id_usuario != p_id_usuario AND 
              id_usuario IN (SELECT id_usuario FROM usuarios WHERE rol = 'operador_supervisor');
        
        IF v_count > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe una sesión activa de operador supervisor.';
        END IF;
    END IF;
    
    -- Actualizar o crear la sesión del usuario actual
    UPDATE sesiones_activas SET ultimo_acceso = NOW() WHERE id_usuario = p_id_usuario AND token = p_token;
END //
DELIMITER ;

-- Procedimiento almacenado para calcular distancia entre direcciones (simple aproximación cartesiana)
DELIMITER //
CREATE FUNCTION calcular_distancia(calle1 INT, carrera1 INT, calle2 INT, carrera2 INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE distancia DECIMAL(10,2);
    SET distancia = SQRT(POW(calle2 - calle1, 2) + POW(carrera2 - carrera1, 2));
    RETURN distancia;
END //
DELIMITER ;

-- Procedimiento almacenado para encontrar vigilantes disponibles para contingencias
DELIMITER //
CREATE PROCEDURE encontrar_vigilantes_disponibles(
    IN p_fecha DATE,
    IN p_hora_inicio TIME,
    IN p_hora_fin TIME,
    IN p_id_edificio INT,
    IN p_horas_minimas_descanso INT
)
BEGIN
    DECLARE v_calle_edificio INT;
    DECLARE v_carrera_edificio INT;
    
    -- Obtener coordenadas del edificio
    SELECT direccion_calle, direccion_carrera INTO v_calle_edificio, v_carrera_edificio
    FROM edificios WHERE id_edificio = p_id_edificio;
    
    -- Encontrar vigilantes disponibles
    SELECT 
        v.id_vigilante,
        v.nombre_completo,
        v.tipo_contrato,
        calcular_distancia(v.direccion_calle, v.direccion_carrera, v_calle_edificio, v_carrera_edificio) AS distancia,
        TIMESTAMPDIFF(HOUR, 
            (SELECT MAX(hora_fin) FROM asignaciones_turnos 
             WHERE id_vigilante = v.id_vigilante AND fecha = p_fecha AND hora_fin <= CONCAT(p_fecha, ' ', p_hora_inicio)),
            CONCAT(p_fecha, ' ', p_hora_inicio)
        ) AS horas_desde_ultimo_turno,
        TIMESTAMPDIFF(HOUR,
            CONCAT(p_fecha, ' ', p_hora_fin),
            (SELECT MIN(hora_inicio) FROM asignaciones_turnos 
             WHERE id_vigilante = v.id_vigilante AND fecha >= p_fecha AND hora_inicio >= CONCAT(p_fecha, ' ', p_hora_fin))
        ) AS horas_hasta_siguiente_turno
    FROM 
        vigilantes v
    LEFT JOIN 
        asignaciones_turnos a ON v.id_vigilante = a.id_vigilante 
            AND ((CONCAT(p_fecha, ' ', p_hora_inicio) BETWEEN a.hora_inicio AND a.hora_fin) 
              OR (CONCAT(p_fecha, ' ', p_hora_fin) BETWEEN a.hora_inicio AND a.hora_fin)
              OR (a.hora_inicio BETWEEN CONCAT(p_fecha, ' ', p_hora_inicio) AND CONCAT(p_fecha, ' ', p_hora_fin)))
    WHERE 
        v.activo = TRUE
        AND a.id_asignacion IS NULL
    GROUP BY 
        v.id_vigilante
    HAVING 
        (horas_desde_ultimo_turno IS NULL OR horas_desde_ultimo_turno >= p_horas_minimas_descanso)
        AND (horas_hasta_siguiente_turno IS NULL OR horas_hasta_siguiente_turno >= p_horas_minimas_descanso)
    ORDER BY 
        -- Priorizar vigilantes part-time, luego por distancia
        CASE WHEN v.tipo_contrato = 'relevo_part_time' THEN 0 ELSE 1 END,
        distancia ASC;
END //
DELIMITER ;

-- Procedimiento almacenado para calcular horas extras
DELIMITER //
CREATE PROCEDURE calcular_horas_extras(IN p_id_asignacion INT)
BEGIN
    DECLARE v_hora_inicio DATETIME;
    DECLARE v_hora_fin DATETIME;
    DECLARE v_fecha DATE;
    DECLARE v_id_vigilante INT;
    DECLARE v_id_edificio INT;
    DECLARE v_es_festivo BOOLEAN DEFAULT FALSE;
    DECLARE v_horas_normales DECIMAL(5,2) DEFAULT 0;
    DECLARE v_horas_extras_diurnas DECIMAL(5,2) DEFAULT 0;
    DECLARE v_horas_extras_nocturnas DECIMAL(5,2) DEFAULT 0;
    DECLARE v_horas_extras_festivas_diurnas DECIMAL(5,2) DEFAULT 0;
    DECLARE v_horas_extras_festivas_nocturnas DECIMAL(5,2) DEFAULT 0;
    
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
    SELECT COUNT(*) > 0 INTO v_es_festivo 
    FROM festivos_colombia 
    WHERE fecha = v_fecha;
    
    -- Lógica para calcular horas normales y extras según los parámetros
    -- Esta es una simplificación, la lógica completa debería tener en cuenta
    -- horarios específicos para extras nocturnas (10pm-6am o 6pm-6am)
    IF v_es_festivo THEN
        -- En festivos, todas las horas son extras festivas
        SET v_horas_extras_festivas_diurnas = TIMESTAMPDIFF(HOUR, v_hora_inicio, v_hora_fin);
    ELSE
        -- En días normales, calcular según horario
        -- Esta es una simplificación, la lógica real sería más compleja
        SET v_horas_normales = TIMESTAMPDIFF(HOUR, v_hora_inicio, v_hora_fin);
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
    ON DUPLICATE KEY UPDATE
        horas_normales = v_horas_normales,
        horas_extras_diurnas = v_horas_extras_diurnas,
        horas_extras_nocturnas = v_horas_extras_nocturnas,
        horas_extras_festivas_diurnas = v_horas_extras_festivas_diurnas,
        horas_extras_festivas_nocturnas = v_horas_extras_festivas_nocturnas,
        es_festivo = v_es_festivo,
        fecha_calculo = NOW();
END //
DELIMITER ;

-- Trigger para calcular horas extras al completar un turno
DELIMITER //
CREATE TRIGGER after_asignacion_completada
AFTER UPDATE ON asignaciones_turnos
FOR EACH ROW
BEGIN
    IF NEW.estado = 'completado' AND OLD.estado != 'completado' THEN
        CALL calcular_horas_extras(NEW.id_asignacion);
    END IF;
END //
DELIMITER ;

-- Vista para ver vigilantes disponibles en un momento dado
CREATE VIEW vista_vigilantes_disponibles AS
SELECT 
    v.id_vigilante,
    v.nombre_completo,
    v.tipo_contrato,
    v.telefono_celular,
    MAX(a.hora_fin) AS ultimo_turno_fin,
    MIN(CASE WHEN a.hora_inicio > NOW() THEN a.hora_inicio ELSE NULL END) AS proximo_turno_inicio
FROM 
    vigilantes v
LEFT JOIN 
    asignaciones_turnos a ON v.id_vigilante = a.id_vigilante AND 
    (a.hora_fin < NOW() OR a.hora_inicio > NOW())
WHERE 
    v.activo = TRUE
GROUP BY 
    v.id_vigilante;

-- Vista para el dashboard de cobertura de edificios
CREATE VIEW vista_cobertura_edificios AS
SELECT 
    e.id_edificio,
    e.nombre AS edificio,
    DATE(a.fecha) AS fecha,
    HOUR(a.hora_inicio) AS hora,
    COUNT(DISTINCT a.id_vigilante) AS vigilantes_asignados
FROM 
    edificios e
LEFT JOIN 
    asignaciones_turnos a ON e.id_edificio = a.id_edificio
WHERE 
    a.fecha BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
GROUP BY 
    e.id_edificio, DATE(a.fecha), HOUR(a.hora_inicio);

-- Creación de usuario administrador por defecto (password: admin123 en MD5)
INSERT INTO usuarios (nombre_usuario, password, rol, nombre_completo, email) 
VALUES ('admin', MD5('admin123'), 'operador_supervisor', 'Administrador Sistema', 'admin@example.com');

-- Configuración inicial del sistema
INSERT INTO configuracion_sistema (minimo_horas_descanso, actualizado_por) 
VALUES (8, 1);
