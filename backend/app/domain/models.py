from datetime import datetime
from typing import List, Optional
from enum import Enum
from dataclasses import dataclass


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ON_LEAVE = "on_leave"


class ShiftTypeEnum(str, Enum):
    NORMAL = "normal"
    OVERTIME = "overtime"
    HOLIDAY = "holiday"
    NIGHT = "night"


@dataclass
class Vigilante:
    """Domain entity for Vigilante (Security Guard)"""
    id: Optional[int]
    name: str
    email: str
    phone: str
    document_id: str
    skills: List[str]
    certifications: List[str]
    status: StatusEnum
    hire_date: datetime
    contract_start: datetime
    contract_end: datetime
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    
    def is_active(self) -> bool:
        return self.status == StatusEnum.ACTIVE
    
    def is_available_for_shift(self, date: datetime) -> bool:
        """Check if vigilante is available for a shift on given date"""
        return (
            self.is_active() and 
            self.contract_start <= date <= self.contract_end
        )


@dataclass
class Building:
    """Domain entity for Building"""
    id: Optional[int]
    name: str
    address: str
    description: Optional[str]
    security_requirements: List[str]
    hourly_rate: float
    overtime_rate: float
    holiday_rate: float
    contact_person: str
    contact_phone: str
    status: StatusEnum
    
    def is_active(self) -> bool:
        return self.status == StatusEnum.ACTIVE


@dataclass
class Shift:
    """Domain entity for Work Shift"""
    id: Optional[int]
    vigilante_id: int
    building_id: int
    start_datetime: datetime
    end_datetime: datetime
    shift_type: ShiftTypeEnum
    notes: Optional[str]
    is_confirmed: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def get_duration_hours(self) -> float:
        """Calculate shift duration in hours"""
        duration = self.end_datetime - self.start_datetime
        return duration.total_seconds() / 3600
    
    def is_overtime(self) -> bool:
        """Check if shift qualifies as overtime"""
        return self.shift_type == ShiftTypeEnum.OVERTIME


@dataclass
class User:
    """Domain entity for System User"""
    id: Optional[int]
    username: str
    email: str
    password_hash: str
    role: str  # "operator" or "auxiliary"
    full_name: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    
    def is_operator(self) -> bool:
        return self.role == "operator"
    
    def is_auxiliary(self) -> bool:
        return self.role == "auxiliary"


@dataclass
class Report:
    """Domain entity for Reports"""
    id: Optional[int]
    title: str
    report_type: str  # "vigilante", "building", "hours"
    criteria: dict
    generated_by: int
    generated_at: datetime
    file_path: Optional[str] = None
    status: str = "pending"  # "pending", "completed", "failed"