"""
Infrastructure layer - Database implementations
This layer implements the repository interfaces defined in the domain layer
"""
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import enum

from ..domain.models import Vigilante, Building, Shift, User, Report, StatusEnum, ShiftTypeEnum
from ..domain.repositories import (
    VigilanteRepository, 
    BuildingRepository, 
    ShiftRepository, 
    UserRepository, 
    ReportRepository
)

Base = declarative_base()

# SQLAlchemy models (Infrastructure models that map to database)
class VigilanteModel(Base):
    __tablename__ = "vigilantes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(50), nullable=False)
    document_id = Column(String(50), unique=True, nullable=False)
    skills = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.ACTIVE)
    hire_date = Column(DateTime, nullable=False)
    contract_start = Column(DateTime, nullable=False)
    contract_end = Column(DateTime, nullable=False)
    address = Column(Text, nullable=True)
    emergency_contact = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BuildingModel(Base):
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    security_requirements = Column(JSON, default=list)
    hourly_rate = Column(Float, nullable=False)
    overtime_rate = Column(Float, nullable=False)
    holiday_rate = Column(Float, nullable=False)
    contact_person = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=False)
    status = Column(SQLEnum(StatusEnum), default=StatusEnum.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ShiftModel(Base):
    __tablename__ = "shifts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    vigilante_id = Column(Integer, nullable=False)  # Foreign key
    building_id = Column(Integer, nullable=False)   # Foreign key
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    shift_type = Column(SQLEnum(ShiftTypeEnum), default=ShiftTypeEnum.NORMAL)
    notes = Column(Text, nullable=True)
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # "operator" or "auxiliary"
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)


class ReportModel(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    report_type = Column(String(100), nullable=False)
    criteria = Column(JSON, nullable=False)
    generated_by = Column(Integer, nullable=False)  # Foreign key to users
    generated_at = Column(DateTime, nullable=False)
    file_path = Column(String(500), nullable=True)
    status = Column(String(50), default="pending")


# Database session management
class DatabaseSession:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        return self.SessionLocal()


# Repository implementations
class SQLVigilanteRepository(VigilanteRepository):
    def __init__(self, db_session: DatabaseSession):
        self.db_session = db_session
    
    def _model_to_entity(self, model: VigilanteModel) -> Vigilante:
        """Convert SQLAlchemy model to domain entity"""
        return Vigilante(
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            document_id=model.document_id,
            skills=model.skills or [],
            certifications=model.certifications or [],
            status=model.status,
            hire_date=model.hire_date,
            contract_start=model.contract_start,
            contract_end=model.contract_end,
            address=model.address,
            emergency_contact=model.emergency_contact
        )
    
    def _entity_to_model(self, entity: Vigilante) -> VigilanteModel:
        """Convert domain entity to SQLAlchemy model"""
        return VigilanteModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            phone=entity.phone,
            document_id=entity.document_id,
            skills=entity.skills,
            certifications=entity.certifications,
            status=entity.status,
            hire_date=entity.hire_date,
            contract_start=entity.contract_start,
            contract_end=entity.contract_end,
            address=entity.address,
            emergency_contact=entity.emergency_contact
        )
    
    def create(self, vigilante: Vigilante) -> Vigilante:
        with self.db_session.get_session() as session:
            model = self._entity_to_model(vigilante)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
    
    def get_by_id(self, vigilante_id: int) -> Optional[Vigilante]:
        with self.db_session.get_session() as session:
            model = session.query(VigilanteModel).filter(VigilanteModel.id == vigilante_id).first()
            return self._model_to_entity(model) if model else None
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Vigilante]:
        with self.db_session.get_session() as session:
            query = session.query(VigilanteModel)
            
            if filters:
                if 'status' in filters:
                    query = query.filter(VigilanteModel.status == filters['status'])
                if 'name' in filters:
                    query = query.filter(VigilanteModel.name.ilike(f"%{filters['name']}%"))
            
            models = query.all()
            return [self._model_to_entity(model) for model in models]
    
    def update(self, vigilante: Vigilante) -> Vigilante:
        with self.db_session.get_session() as session:
            model = session.query(VigilanteModel).filter(VigilanteModel.id == vigilante.id).first()
            if model:
                model.name = vigilante.name
                model.email = vigilante.email
                model.phone = vigilante.phone
                model.document_id = vigilante.document_id
                model.skills = vigilante.skills
                model.certifications = vigilante.certifications
                model.status = vigilante.status
                model.hire_date = vigilante.hire_date
                model.contract_start = vigilante.contract_start
                model.contract_end = vigilante.contract_end
                model.address = vigilante.address
                model.emergency_contact = vigilante.emergency_contact
                model.updated_at = datetime.utcnow()
                
                session.commit()
                session.refresh(model)
                return self._model_to_entity(model)
    
    def delete(self, vigilante_id: int) -> bool:
        with self.db_session.get_session() as session:
            model = session.query(VigilanteModel).filter(VigilanteModel.id == vigilante_id).first()
            if model:
                session.delete(model)
                session.commit()
                return True
            return False
    
    def get_by_email(self, email: str) -> Optional[Vigilante]:
        with self.db_session.get_session() as session:
            model = session.query(VigilanteModel).filter(VigilanteModel.email == email).first()
            return self._model_to_entity(model) if model else None
    
    def get_active_vigilantes(self) -> List[Vigilante]:
        return self.get_all({'status': StatusEnum.ACTIVE})


class SQLBuildingRepository(BuildingRepository):
    def __init__(self, db_session: DatabaseSession):
        self.db_session = db_session
    
    def _model_to_entity(self, model: BuildingModel) -> Building:
        return Building(
            id=model.id,
            name=model.name,
            address=model.address,
            description=model.description,
            security_requirements=model.security_requirements or [],
            hourly_rate=model.hourly_rate,
            overtime_rate=model.overtime_rate,
            holiday_rate=model.holiday_rate,
            contact_person=model.contact_person,
            contact_phone=model.contact_phone,
            status=model.status
        )
    
    def _entity_to_model(self, entity: Building) -> BuildingModel:
        return BuildingModel(
            id=entity.id,
            name=entity.name,
            address=entity.address,
            description=entity.description,
            security_requirements=entity.security_requirements,
            hourly_rate=entity.hourly_rate,
            overtime_rate=entity.overtime_rate,
            holiday_rate=entity.holiday_rate,
            contact_person=entity.contact_person,
            contact_phone=entity.contact_phone,
            status=entity.status
        )
    
    def create(self, building: Building) -> Building:
        with self.db_session.get_session() as session:
            model = self._entity_to_model(building)
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
    
    def get_by_id(self, building_id: int) -> Optional[Building]:
        with self.db_session.get_session() as session:
            model = session.query(BuildingModel).filter(BuildingModel.id == building_id).first()
            return self._model_to_entity(model) if model else None
    
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Building]:
        with self.db_session.get_session() as session:
            query = session.query(BuildingModel)
            
            if filters:
                if 'status' in filters:
                    query = query.filter(BuildingModel.status == filters['status'])
                if 'name' in filters:
                    query = query.filter(BuildingModel.name.ilike(f"%{filters['name']}%"))
            
            models = query.all()
            return [self._model_to_entity(model) for model in models]
    
    def update(self, building: Building) -> Building:
        with self.db_session.get_session() as session:
            model = session.query(BuildingModel).filter(BuildingModel.id == building.id).first()
            if model:
                model.name = building.name
                model.address = building.address
                model.description = building.description
                model.security_requirements = building.security_requirements
                model.hourly_rate = building.hourly_rate
                model.overtime_rate = building.overtime_rate
                model.holiday_rate = building.holiday_rate
                model.contact_person = building.contact_person
                model.contact_phone = building.contact_phone
                model.status = building.status
                model.updated_at = datetime.utcnow()
                
                session.commit()
                session.refresh(model)
                return self._model_to_entity(model)
    
    def delete(self, building_id: int) -> bool:
        with self.db_session.get_session() as session:
            model = session.query(BuildingModel).filter(BuildingModel.id == building_id).first()
            if model:
                session.delete(model)
                session.commit()
                return True
            return False
    
    def get_active_buildings(self) -> List[Building]:
        return self.get_all({'status': StatusEnum.ACTIVE})


class SQLUserRepository(UserRepository):
    """SQLAlchemy implementation of UserRepository"""
    
    def __init__(self, db_session: DatabaseSession):
        self.db_session = db_session
    
    def _model_to_entity(self, model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity"""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            full_name=model.full_name,
            is_active=model.is_active,
            created_at=model.created_at,
            last_login=model.last_login
        )
    
    def _entity_to_model(self, user: User) -> UserModel:
        """Convert domain entity to SQLAlchemy model"""
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            last_login=user.last_login
        )
    
    def create(self, user: User) -> User:
        with self.db_session.get_session() as session:
            model = self._entity_to_model(user)
            model.id = None  # Let the database assign the ID
            model.created_at = datetime.utcnow()
            
            session.add(model)
            session.commit()
            session.refresh(model)
            return self._model_to_entity(model)
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db_session.get_session() as session:
            model = session.query(UserModel).filter(UserModel.id == user_id).first()
            return self._model_to_entity(model) if model else None
    
    def get_by_username(self, username: str) -> Optional[User]:
        with self.db_session.get_session() as session:
            model = session.query(UserModel).filter(UserModel.username == username).first()
            return self._model_to_entity(model) if model else None
    
    def get_by_email(self, email: str) -> Optional[User]:
        with self.db_session.get_session() as session:
            model = session.query(UserModel).filter(UserModel.email == email).first()
            return self._model_to_entity(model) if model else None
    
    def update(self, user: User) -> User:
        with self.db_session.get_session() as session:
            model = session.query(UserModel).filter(UserModel.id == user.id).first()
            if model:
                model.username = user.username
                model.email = user.email
                model.password_hash = user.password_hash
                model.role = user.role
                model.full_name = user.full_name
                model.is_active = user.is_active
                model.last_login = user.last_login
                
                session.commit()
                session.refresh(model)
                return self._model_to_entity(model)
    
    def delete(self, user_id: int) -> bool:
        with self.db_session.get_session() as session:
            model = session.query(UserModel).filter(UserModel.id == user_id).first()
            if model:
                session.delete(model)
                session.commit()
                return True
            return False


# Legacy function for compatibility
def get_db():
    """Legacy function - to be replaced with DatabaseSession"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    DATABASE_URL = "postgresql://user:password@localhost/dbname"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()