"""
Database models and configuration for SchedulesApp
Implements SQLAlchemy models that map to PostgreDB.sql schema
"""

from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, DateTime, Time, Text, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime, date
import os

Base = declarative_base()

# Database Configuration
def get_database_url():
    """Get database URL from environment variables"""
    return os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/gestion_turnos_vigilantes')

def create_engine_instance():
    """Create and return SQLAlchemy engine"""
    database_url = get_database_url()
    return create_engine(database_url, echo=False)

def get_session():
    """Create and return database session"""
    engine = create_engine_instance()
    Session = sessionmaker(bind=engine)
    return Session()

def create_tables():
    """Create all tables in the database"""
    engine = create_engine_instance()
    Base.metadata.create_all(engine)

# User Management Models
class UserModel(Base):
    """Users table - usuarios"""
    __tablename__ = 'usuarios'
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    rol = Column(String(50), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=func.now())
    ultima_sesion = Column(DateTime)
    
    __table_args__ = (
        CheckConstraint("rol IN ('operador_supervisor', 'auxiliar_administrativo')"),
    )

# Vigilantes Management Models
class VigilanteModel(Base):
    """Vigilantes table - vigilantes"""
    __tablename__ = 'vigilantes'
    
    id_vigilante = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    numero_identificacion = Column(String(20), nullable=False, unique=True)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono_celular = Column(String(20), nullable=False)
    correo_electronico = Column(String(100))
    direccion_calle = Column(Integer, nullable=False)
    direccion_carrera = Column(Integer, nullable=False)
    direccion_completa = Column(String(255), nullable=False)
    contacto_emergencia_nombre = Column(String(100), nullable=False)
    contacto_emergencia_telefono = Column(String(20), nullable=False)
    tipo_contrato = Column(String(50), nullable=False)
    edificios = Column(String(50), nullable=False)
    salario = Column(DECIMAL(10, 2), nullable=False)
    fecha_contratacion = Column(Date, nullable=False)
    foto = Column(Text)  # BYTEA equivalent for photos
    activo = Column(Boolean, default=True)
    
    __table_args__ = (
        CheckConstraint("tipo_contrato IN ('fijo_full_time', 'relevo_part_time')"),
    )

class CertificacionVigilanteModel(Base):
    """Vigilante certifications table - certificaciones_vigilantes"""
    __tablename__ = 'certificaciones_vigilantes'
    
    id_certificacion = Column(Integer, primary_key=True, autoincrement=True)
    id_vigilante = Column(Integer, ForeignKey('vigilantes.id_vigilante', ondelete='CASCADE'), nullable=False)
    curso_vigilancia = Column(Boolean, default=False)
    manejo_armas = Column(Boolean, default=False)
    medios_electronicos = Column(Boolean, default=False)
    primeros_auxilios = Column(Boolean, default=False)
    fecha_actualizacion = Column(DateTime, default=func.now())
    
    # Relationship
    vigilante = relationship("VigilanteModel", backref="certificaciones")

# Buildings Management Models
class BuildingModel(Base):
    """Buildings table - edificios"""
    __tablename__ = 'edificios'
    
    id_edificio = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion_calle = Column(Integer, nullable=False)
    direccion_carrera = Column(Integer, nullable=False)
    direccion_completa = Column(String(255), nullable=False)
    telefono = Column(String(20))
    administrador = Column(String(100))
    telefono_administrador = Column(String(20))
    tipo_turno = Column(String(20), nullable=False)
    horas_semanales = Column(Integer, nullable=False)
    activo = Column(Boolean, default=True)
    
    __table_args__ = (
        CheckConstraint("tipo_turno IN ('8_horas', '12_horas', '24_horas')"),
        CheckConstraint("horas_semanales >= 40 AND horas_semanales <= 48"),
    )

# Shift Types and Planning Models
class TipoTurnoModel(Base):
    """Shift types table - tipos_turnos"""
    __tablename__ = 'tipos_turnos'
    
    id_tipo_turno = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    duracion = Column(Integer, nullable=False)
    descripcion = Column(String(255))

class PlanillaTurnoModel(Base):
    """Monthly shift planning table - planilla_turnos"""
    __tablename__ = 'planilla_turnos'
    
    id_planilla = Column(Integer, primary_key=True, autoincrement=True)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    fecha_generacion = Column(DateTime, default=func.now())
    generado_por = Column(Integer, ForeignKey('usuarios.id_usuario'))
    estado = Column(String(20), default='borrador')
    
    __table_args__ = (
        CheckConstraint("mes >= 1 AND mes <= 12"),
        CheckConstraint("estado IN ('borrador', 'publicado', 'archivado')"),
    )

class ShiftModel(Base):
    """Shift assignments table - asignaciones_turnos"""
    __tablename__ = 'asignaciones_turnos'
    
    id_asignacion = Column(Integer, primary_key=True, autoincrement=True)
    id_planilla = Column(Integer, ForeignKey('planilla_turnos.id_planilla'), nullable=False)
    id_vigilante = Column(Integer, ForeignKey('vigilantes.id_vigilante'), nullable=False)
    id_edificio = Column(Integer, ForeignKey('edificios.id_edificio'), nullable=False)
    id_tipo_turno = Column(Integer, ForeignKey('tipos_turnos.id_tipo_turno'), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=False)
    es_turno_habitual = Column(Boolean, default=True)
    estado = Column(String(20), default='programado')
    creado_por = Column(Integer, ForeignKey('usuarios.id_usuario'))
    fecha_creacion = Column(DateTime, default=func.now())
    
    # Relationships
    planilla = relationship("PlanillaTurnoModel")
    vigilante = relationship("VigilanteModel")
    edificio = relationship("BuildingModel")
    tipo_turno = relationship("TipoTurnoModel")
    
    __table_args__ = (
        CheckConstraint("estado IN ('programado', 'confirmado', 'completado', 'ausente')"),
    )

# Contingencies and Incidents Models
class NovedadModel(Base):
    """Incidents and contingencies table - novedades"""
    __tablename__ = 'novedades'
    
    id_novedad = Column(Integer, primary_key=True, autoincrement=True)
    id_asignacion_original = Column(Integer, ForeignKey('asignaciones_turnos.id_asignacion'))
    id_vigilante_original = Column(Integer, ForeignKey('vigilantes.id_vigilante'), nullable=False)
    id_vigilante_reemplazo = Column(Integer, ForeignKey('vigilantes.id_vigilante'))
    id_edificio = Column(Integer, ForeignKey('edificios.id_edificio'), nullable=False)
    fecha_novedad = Column(Date, nullable=False)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=False)
    tipo_novedad = Column(String(50), nullable=False)
    descripcion = Column(Text)
    estado = Column(String(20), default='pendiente')
    registrado_por = Column(Integer, ForeignKey('usuarios.id_usuario'))
    fecha_registro = Column(DateTime, default=func.now())
    
    # Relationships
    asignacion_original = relationship("ShiftModel")
    vigilante_original = relationship("VigilanteModel", foreign_keys=[id_vigilante_original])
    vigilante_reemplazo = relationship("VigilanteModel", foreign_keys=[id_vigilante_reemplazo])
    edificio = relationship("BuildingModel")
    
    __table_args__ = (
        CheckConstraint("tipo_novedad IN ('incapacidad', 'ausencia', 'contingencia', 'despido', 'calamidad', 'permiso', 'vacaciones', 'solicitud_vigilante')"),
        CheckConstraint("estado IN ('pendiente', 'resuelta', 'cancelada')"),
    )

# Hours Registration and Payroll Models
class RegistroHorasModel(Base):
    """Hours registration table - registro_horas"""
    __tablename__ = 'registro_horas'
    
    id_registro = Column(Integer, primary_key=True, autoincrement=True)
    id_asignacion = Column(Integer, ForeignKey('asignaciones_turnos.id_asignacion'), nullable=False)
    id_vigilante = Column(Integer, ForeignKey('vigilantes.id_vigilante'), nullable=False)
    id_edificio = Column(Integer, ForeignKey('edificios.id_edificio'), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(DateTime, nullable=False)
    hora_fin = Column(DateTime, nullable=False)
    horas_normales = Column(DECIMAL(5, 2), default=0)
    horas_extras = Column(DECIMAL(5, 2), default=0)
    horas_festivas = Column(DECIMAL(5, 2), default=0)
    observaciones = Column(Text)
    registrado_por = Column(Integer, ForeignKey('usuarios.id_usuario'))
    fecha_registro = Column(DateTime, default=func.now())
    
    # Relationships
    asignacion = relationship("ShiftModel")
    vigilante = relationship("VigilanteModel")
    edificio = relationship("BuildingModel")

# System Configuration Model
class ConfiguracionSistemaModel(Base):
    """System configuration table - configuracion_sistema"""
    __tablename__ = 'configuracion_sistema'
    
    id_configuracion = Column(Integer, primary_key=True, autoincrement=True)
    minimo_horas_descanso = Column(Integer, nullable=False, default=8)
    ultimo_backup = Column(Date)
    ultima_limpieza_trimestral = Column(Date)
    actualizado_por = Column(Integer, ForeignKey('usuarios.id_usuario'))
    fecha_actualizacion = Column(DateTime, default=func.now())
    
    __table_args__ = (
        CheckConstraint("minimo_horas_descanso >= 1 AND minimo_horas_descanso <= 12"),
    )

# Repository Base Classes for Clean Architecture
from abc import ABC, abstractmethod
from typing import List, Optional

class UserRepository(ABC):
    """Abstract repository for User operations"""
    
    @abstractmethod
    def create(self, user_data: dict) -> dict:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[dict]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[dict]:
        pass
    
    @abstractmethod
    def update(self, user_id: int, user_data: dict) -> dict:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass

class VigilanteRepository(ABC):
    """Abstract repository for Vigilante operations"""
    
    @abstractmethod
    def create(self, vigilante_data: dict) -> dict:
        pass
    
    @abstractmethod
    def get_all(self) -> List[dict]:
        pass
    
    @abstractmethod
    def get_by_id(self, vigilante_id: int) -> Optional[dict]:
        pass
    
    @abstractmethod
    def update(self, vigilante_id: int, vigilante_data: dict) -> dict:
        pass
    
    @abstractmethod
    def delete(self, vigilante_id: int) -> bool:
        pass

class BuildingRepository(ABC):
    """Abstract repository for Building operations"""
    
    @abstractmethod
    def create(self, building_data: dict) -> dict:
        pass
    
    @abstractmethod
    def get_all(self) -> List[dict]:
        pass
    
    @abstractmethod
    def get_by_id(self, building_id: int) -> Optional[dict]:
        pass
    
    @abstractmethod
    def update(self, building_id: int, building_data: dict) -> dict:
        pass
    
    @abstractmethod
    def delete(self, building_id: int) -> bool:
        pass

# SQLAlchemy Repository Implementations
class SQLUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository"""
    
    def __init__(self):
        self.session = get_session()
    
    def create(self, user_data: dict) -> dict:
        """Create a new user"""
        user_model = UserModel(
            nombre_usuario=user_data['username'],
            password=user_data['password'],
            rol=user_data['role'],
            nombre_completo=user_data['full_name'],
            email=user_data['email']
        )
        self.session.add(user_model)
        self.session.commit()
        return self._model_to_entity(user_model)
    
    def get_by_id(self, user_id: int) -> Optional[dict]:
        """Get user by ID"""
        user_model = self.session.query(UserModel).filter(UserModel.id_usuario == user_id).first()
        return self._model_to_entity(user_model) if user_model else None
    
    def get_by_username(self, username: str) -> Optional[dict]:
        """Get user by username"""
        user_model = self.session.query(UserModel).filter(UserModel.nombre_usuario == username).first()
        return self._model_to_entity(user_model) if user_model else None
    
    def update(self, user_id: int, user_data: dict) -> dict:
        """Update user data"""
        user_model = self.session.query(UserModel).filter(UserModel.id_usuario == user_id).first()
        if user_model:
            for key, value in user_data.items():
                if hasattr(user_model, key):
                    setattr(user_model, key, value)
            self.session.commit()
            return self._model_to_entity(user_model)
        return None
    
    def delete(self, user_id: int) -> bool:
        """Delete user"""
        user_model = self.session.query(UserModel).filter(UserModel.id_usuario == user_id).first()
        if user_model:
            self.session.delete(user_model)
            self.session.commit()
            return True
        return False
    
    def _model_to_entity(self, model: UserModel) -> dict:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        return {
            'id': model.id_usuario,
            'username': model.nombre_usuario,
            'password': model.password,
            'role': model.rol,
            'full_name': model.nombre_completo,
            'email': model.email,
            'active': model.activo,
            'created_at': model.fecha_creacion,
            'last_session': model.ultima_sesion
        }

class SQLVigilanteRepository(VigilanteRepository):
    """SQLAlchemy implementation of VigilanteRepository"""
    
    def __init__(self):
        self.session = get_session()
    
    def create(self, vigilante_data: dict) -> dict:
        """Create a new vigilante"""
        vigilante_model = VigilanteModel(
            nombre_completo=vigilante_data['full_name'],
            numero_identificacion=vigilante_data['identification_number'],
            fecha_nacimiento=vigilante_data['birth_date'],
            telefono_celular=vigilante_data['phone'],
            correo_electronico=vigilante_data.get('email'),
            direccion_calle=vigilante_data['street_number'],
            direccion_carrera=vigilante_data['avenue_number'],
            direccion_completa=vigilante_data['full_address'],
            contacto_emergencia_nombre=vigilante_data['emergency_contact_name'],
            contacto_emergencia_telefono=vigilante_data['emergency_contact_phone'],
            tipo_contrato=vigilante_data['contract_type'],
            edificios=vigilante_data['buildings'],
            salario=vigilante_data['salary'],
            fecha_contratacion=vigilante_data['hire_date']
        )
        self.session.add(vigilante_model)
        self.session.commit()
        return self._model_to_entity(vigilante_model)
    
    def get_all(self) -> List[dict]:
        """Get all vigilantes"""
        vigilantes = self.session.query(VigilanteModel).filter(VigilanteModel.activo == True).all()
        return [self._model_to_entity(v) for v in vigilantes]
    
    def get_by_id(self, vigilante_id: int) -> Optional[dict]:
        """Get vigilante by ID"""
        vigilante_model = self.session.query(VigilanteModel).filter(VigilanteModel.id_vigilante == vigilante_id).first()
        return self._model_to_entity(vigilante_model) if vigilante_model else None
    
    def update(self, vigilante_id: int, vigilante_data: dict) -> dict:
        """Update vigilante data"""
        vigilante_model = self.session.query(VigilanteModel).filter(VigilanteModel.id_vigilante == vigilante_id).first()
        if vigilante_model:
            for key, value in vigilante_data.items():
                if hasattr(vigilante_model, key):
                    setattr(vigilante_model, key, value)
            self.session.commit()
            return self._model_to_entity(vigilante_model)
        return None
    
    def delete(self, vigilante_id: int) -> bool:
        """Soft delete vigilante"""
        vigilante_model = self.session.query(VigilanteModel).filter(VigilanteModel.id_vigilante == vigilante_id).first()
        if vigilante_model:
            vigilante_model.activo = False
            self.session.commit()
            return True
        return False
    
    def _model_to_entity(self, model: VigilanteModel) -> dict:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        return {
            'id': model.id_vigilante,
            'full_name': model.nombre_completo,
            'identification_number': model.numero_identificacion,
            'birth_date': model.fecha_nacimiento,
            'phone': model.telefono_celular,
            'email': model.correo_electronico,
            'street_number': model.direccion_calle,
            'avenue_number': model.direccion_carrera,
            'full_address': model.direccion_completa,
            'emergency_contact_name': model.contacto_emergencia_nombre,
            'emergency_contact_phone': model.contacto_emergencia_telefono,
            'contract_type': model.tipo_contrato,
            'buildings': model.edificios,
            'salary': float(model.salario),
            'hire_date': model.fecha_contratacion,
            'active': model.activo
        }

class SQLBuildingRepository(BuildingRepository):
    """SQLAlchemy implementation of BuildingRepository"""
    
    def __init__(self):
        self.session = get_session()
    
    def create(self, building_data: dict) -> dict:
        """Create a new building"""
        building_model = BuildingModel(
            nombre=building_data['name'],
            direccion_calle=building_data['street_number'],
            direccion_carrera=building_data['avenue_number'],
            direccion_completa=building_data['full_address'],
            telefono=building_data.get('phone'),
            administrador=building_data.get('administrator'),
            telefono_administrador=building_data.get('administrator_phone'),
            tipo_turno=building_data['shift_type'],
            horas_semanales=building_data['weekly_hours']
        )
        self.session.add(building_model)
        self.session.commit()
        return self._model_to_entity(building_model)
    
    def get_all(self) -> List[dict]:
        """Get all buildings"""
        buildings = self.session.query(BuildingModel).filter(BuildingModel.activo == True).all()
        return [self._model_to_entity(b) for b in buildings]
    
    def get_by_id(self, building_id: int) -> Optional[dict]:
        """Get building by ID"""
        building_model = self.session.query(BuildingModel).filter(BuildingModel.id_edificio == building_id).first()
        return self._model_to_entity(building_model) if building_model else None
    
    def update(self, building_id: int, building_data: dict) -> dict:
        """Update building data"""
        building_model = self.session.query(BuildingModel).filter(BuildingModel.id_edificio == building_id).first()
        if building_model:
            for key, value in building_data.items():
                if hasattr(building_model, key):
                    setattr(building_model, key, value)
            self.session.commit()
            return self._model_to_entity(building_model)
        return None
    
    def delete(self, building_id: int) -> bool:
        """Soft delete building"""
        building_model = self.session.query(BuildingModel).filter(BuildingModel.id_edificio == building_id).first()
        if building_model:
            building_model.activo = False
            self.session.commit()
            return True
        return False
    
    def _model_to_entity(self, model: BuildingModel) -> dict:
        """Convert SQLAlchemy model to domain entity"""
        if not model:
            return None
        return {
            'id': model.id_edificio,
            'name': model.nombre,
            'street_number': model.direccion_calle,
            'avenue_number': model.direccion_carrera,
            'full_address': model.direccion_completa,
            'phone': model.telefono,
            'administrator': model.administrador,
            'administrator_phone': model.telefono_administrador,
            'shift_type': model.tipo_turno,
            'weekly_hours': model.horas_semanales,
            'active': model.activo
        }
