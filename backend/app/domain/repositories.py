"""
Repository interfaces for Clean Architecture
These define the contracts that infrastructure layer must implement
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .models import Vigilante, Building, Shift, User, Report


class VigilanteRepository(ABC):
    """Repository interface for Vigilante operations"""
    
    @abstractmethod
    def create(self, vigilante: Vigilante) -> Vigilante:
        pass
    
    @abstractmethod
    def get_by_id(self, vigilante_id: int) -> Optional[Vigilante]:
        pass
    
    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Vigilante]:
        pass
    
    @abstractmethod
    def update(self, vigilante: Vigilante) -> Vigilante:
        pass
    
    @abstractmethod
    def delete(self, vigilante_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Vigilante]:
        pass
    
    @abstractmethod
    def get_active_vigilantes(self) -> List[Vigilante]:
        pass


class BuildingRepository(ABC):
    """Repository interface for Building operations"""
    
    @abstractmethod
    def create(self, building: Building) -> Building:
        pass
    
    @abstractmethod
    def get_by_id(self, building_id: int) -> Optional[Building]:
        pass
    
    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Building]:
        pass
    
    @abstractmethod
    def update(self, building: Building) -> Building:
        pass
    
    @abstractmethod
    def delete(self, building_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_active_buildings(self) -> List[Building]:
        pass


class ShiftRepository(ABC):
    """Repository interface for Shift operations"""
    
    @abstractmethod
    def create(self, shift: Shift) -> Shift:
        pass
    
    @abstractmethod
    def get_by_id(self, shift_id: int) -> Optional[Shift]:
        pass
    
    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Shift]:
        pass
    
    @abstractmethod
    def update(self, shift: Shift) -> Shift:
        pass
    
    @abstractmethod
    def delete(self, shift_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_shifts_by_vigilante(self, vigilante_id: int) -> List[Shift]:
        pass
    
    @abstractmethod
    def get_shifts_by_building(self, building_id: int) -> List[Shift]:
        pass
    
    @abstractmethod
    def get_shifts_by_date_range(self, start_date, end_date) -> List[Shift]:
        pass


class UserRepository(ABC):
    """Repository interface for User operations"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        pass


class ReportRepository(ABC):
    """Repository interface for Report operations"""
    
    @abstractmethod
    def create(self, report: Report) -> Report:
        pass
    
    @abstractmethod
    def get_by_id(self, report_id: int) -> Optional[Report]:
        pass
    
    @abstractmethod
    def get_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Report]:
        pass
    
    @abstractmethod
    def update(self, report: Report) -> Report:
        pass
    
    @abstractmethod
    def delete(self, report_id: int) -> bool:
        pass
    
    @abstractmethod
    def generate_vigilante_report(self, vigilante_id: int, start_date, end_date) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_building_report(self, building_id: int, start_date, end_date) -> Dict[str, Any]:
        pass
