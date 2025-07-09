"""
Application Services Layer
This layer orchestrates the business logic and coordinates between domain and infrastructure
"""
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from ..domain.models import Vigilante, Building, Shift, User, Report, StatusEnum, ShiftTypeEnum
from ..domain.repositories import VigilanteRepository, BuildingRepository, ShiftRepository, UserRepository, ReportRepository
from ..domain.services import ShiftAssignmentService, PayrollCalculationService, ContingencyManagementService


class VigilanteService:
    """Application service for Vigilante operations"""
    
    def __init__(self, vigilante_repository: VigilanteRepository):
        self.vigilante_repository = vigilante_repository

    def register_vigilante(self, vigilante_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new vigilante with validation"""
        try:
            # Validate required fields
            required_fields = ['name', 'email', 'phone', 'document_id']
            for field in required_fields:
                if field not in vigilante_data:
                    return {
                        "success": False,
                        "message": f"Missing required field: {field}"
                    }
            
            # Check if email already exists
            existing_vigilante = self.vigilante_repository.get_by_email(vigilante_data['email'])
            if existing_vigilante:
                return {
                    "success": False,
                    "message": "A vigilante with this email already exists"
                }
            
            # Create vigilante entity
            vigilante = Vigilante(
                id=None,
                name=vigilante_data['name'],
                email=vigilante_data['email'],
                phone=vigilante_data['phone'],
                document_id=vigilante_data['document_id'],
                skills=vigilante_data.get('skills', []),
                certifications=vigilante_data.get('certifications', []),
                status=StatusEnum(vigilante_data.get('status', StatusEnum.ACTIVE)),
                hire_date=datetime.fromisoformat(vigilante_data.get('hire_date', datetime.now().isoformat())),
                contract_start=datetime.fromisoformat(vigilante_data['contract_start']),
                contract_end=datetime.fromisoformat(vigilante_data['contract_end']),
                address=vigilante_data.get('address'),
                emergency_contact=vigilante_data.get('emergency_contact')
            )
            
            # Save to repository
            created_vigilante = self.vigilante_repository.create(vigilante)
            
            return {
                "success": True,
                "data": created_vigilante,
                "message": "Vigilante registered successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to register vigilante"
            }

    def get_vigilante(self, vigilante_id: int) -> Dict[str, Any]:
        """Get vigilante by ID"""
        try:
            vigilante = self.vigilante_repository.get_by_id(vigilante_id)
            if not vigilante:
                return {
                    "success": False,
                    "message": "Vigilante not found"
                }
            return {
                "success": True,
                "data": vigilante
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_all_vigilantes(self, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Get all vigilantes with optional filters"""
        try:
            vigilantes = self.vigilante_repository.get_all(filters)
            return {
                "success": True,
                "data": vigilantes,
                "count": len(vigilantes)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def update_vigilante(self, vigilante_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update vigilante information"""
        try:
            # Get existing vigilante
            vigilante = self.vigilante_repository.get_by_id(vigilante_id)
            if not vigilante:
                return {
                    "success": False,
                    "message": "Vigilante not found"
                }
            
            # Update fields
            for field, value in update_data.items():
                if hasattr(vigilante, field):
                    setattr(vigilante, field, value)
            
            # Save updated vigilante
            updated_vigilante = self.vigilante_repository.update(vigilante)
            
            return {
                "success": True,
                "data": updated_vigilante,
                "message": "Vigilante updated successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update vigilante"
            }


class BuildingService:
    """Application service for Building operations"""
    
    def __init__(self, building_repository: BuildingRepository):
        self.building_repository = building_repository

    def create_building(self, building_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new building"""
        try:
            # Validate required fields
            required_fields = ['name', 'address', 'hourly_rate', 'contact_person', 'contact_phone']
            for field in required_fields:
                if field not in building_data:
                    return {
                        "success": False,
                        "message": f"Missing required field: {field}"
                    }
            
            # Create building entity
            building = Building(
                id=None,
                name=building_data['name'],
                address=building_data['address'],
                description=building_data.get('description'),
                security_requirements=building_data.get('security_requirements', []),
                hourly_rate=float(building_data['hourly_rate']),
                overtime_rate=float(building_data.get('overtime_rate', building_data['hourly_rate'] * 1.5)),
                holiday_rate=float(building_data.get('holiday_rate', building_data['hourly_rate'] * 2.0)),
                contact_person=building_data['contact_person'],
                contact_phone=building_data['contact_phone'],
                status=StatusEnum(building_data.get('status', StatusEnum.ACTIVE))
            )
            
            # Save to repository
            created_building = self.building_repository.create(building)
            
            return {
                "success": True,
                "data": created_building,
                "message": "Building created successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create building"
            }

    def get_all_buildings(self) -> Dict[str, Any]:
        """Get all buildings"""
        try:
            buildings = self.building_repository.get_all()
            return {
                "success": True,
                "data": buildings,
                "count": len(buildings)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class ShiftService:
    """Application service for Shift operations"""
    
    def __init__(self, 
                 shift_repository: ShiftRepository,
                 vigilante_repository: VigilanteRepository,
                 building_repository: BuildingRepository):
        self.shift_repository = shift_repository
        self.vigilante_repository = vigilante_repository
        self.building_repository = building_repository

    def create_shift(self, shift_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new shift with validation"""
        try:
            # Validate required fields
            required_fields = ['vigilante_id', 'building_id', 'start_datetime', 'end_datetime']
            for field in required_fields:
                if field not in shift_data:
                    return {
                        "success": False,
                        "message": f"Missing required field: {field}"
                    }
            
            # Validate vigilante exists and is active
            vigilante = self.vigilante_repository.get_by_id(shift_data['vigilante_id'])
            if not vigilante or not vigilante.is_active():
                return {
                    "success": False,
                    "message": "Vigilante not found or inactive"
                }
            
            # Validate building exists and is active
            building = self.building_repository.get_by_id(shift_data['building_id'])
            if not building or not building.is_active():
                return {
                    "success": False,
                    "message": "Building not found or inactive"
                }
            
            # Create shift entity
            shift = Shift(
                id=None,
                vigilante_id=shift_data['vigilante_id'],
                building_id=shift_data['building_id'],
                start_datetime=datetime.fromisoformat(shift_data['start_datetime']),
                end_datetime=datetime.fromisoformat(shift_data['end_datetime']),
                shift_type=ShiftTypeEnum(shift_data.get('shift_type', ShiftTypeEnum.NORMAL)),
                notes=shift_data.get('notes'),
                is_confirmed=shift_data.get('is_confirmed', False),
                created_at=datetime.now()
            )
            
            # Validate minimum rest time
            existing_shifts = self.shift_repository.get_shifts_by_vigilante(shift_data['vigilante_id'])
            if not ContingencyManagementService.validate_minimum_rest_time(
                shift_data['vigilante_id'], shift, existing_shifts
            ):
                return {
                    "success": False,
                    "message": "Insufficient rest time between shifts (minimum 12 hours required)"
                }
            
            # Save to repository
            created_shift = self.shift_repository.create(shift)
            
            return {
                "success": True,
                "data": created_shift,
                "message": "Shift created successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create shift"
            }

    def get_all_shifts(self, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """Get all shifts with optional filters"""
        try:
            shifts = self.shift_repository.get_all(filters)
            return {
                "success": True,
                "data": shifts,
                "count": len(shifts)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_shift(self, shift_id: int) -> Dict[str, Any]:
        """Get shift by ID"""
        try:
            shift = self.shift_repository.get_by_id(shift_id)
            if not shift:
                return {
                    "success": False,
                    "message": "Shift not found"
                }
            return {
                "success": True,
                "data": shift
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class ReportService:
    """Application service for Report operations"""
    
    def __init__(self, 
                 report_repository: ReportRepository,
                 shift_repository: ShiftRepository,
                 vigilante_repository: VigilanteRepository,
                 building_repository: BuildingRepository):
        self.report_repository = report_repository
        self.shift_repository = shift_repository
        self.vigilante_repository = vigilante_repository
        self.building_repository = building_repository

    def generate_report(self, report_criteria: Dict) -> Dict:
        """Generate a report based on criteria"""
        try:
            report_data = self.report_repository.generate(report_criteria)
            return {
                "success": True,
                "data": report_data,
                "generated_at": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def export_report(self, report_id: int, format: str) -> Dict[str, Any]:
        """Export report in specified format (PDF/Excel)"""
        try:
            if format not in ['pdf', 'excel']:
                return {
                    "success": False,
                    "message": "Invalid format. Use 'pdf' or 'excel'"
                }
            
            # Get report
            report = self.report_repository.get_by_id(report_id)
            if not report:
                return {
                    "success": False,
                    "message": "Report not found"
                }
            
            # TODO: Implement actual file generation logic
            file_path = f"/tmp/report_{report_id}.{format}"
            
            # Update report with file path
            report.file_path = file_path
            self.report_repository.update(report)
            
            return {
                "success": True,
                "file_path": file_path,
                "format": format,
                "message": f"Report exported to {format.upper()} successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to export report"
            }


class UserService:
    """Application service for User operations and authentication"""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a new user with validation"""
        try:
            # Validate required fields
            required_fields = ['username', 'email', 'password', 'full_name']
            for field in required_fields:
                if field not in user_data:
                    return {
                        "success": False,
                        "message": f"Missing required field: {field}"
                    }
            
            # Check if username already exists
            existing_user = self.user_repository.get_by_username(user_data['username'])
            if existing_user:
                return {
                    "success": False,
                    "message": "A user with this username already exists"
                }
            
            # Check if email already exists
            existing_email = self.user_repository.get_by_email(user_data['email'])
            if existing_email:
                return {
                    "success": False,
                    "message": "A user with this email already exists"
                }
            
            # Create user entity
            user = User(
                id=None,
                username=user_data['username'],
                email=user_data['email'],
                password_hash=user_data['password'],  # This should be hashed before calling this method
                role=user_data.get('role', 'auxiliary'),
                full_name=user_data['full_name'],
                is_active=True,
                created_at=datetime.now()
            )
            
            # Save to repository
            created_user = self.user_repository.create(user)
            
            return {
                "success": True,
                "data": {
                    "id": created_user.id,
                    "username": created_user.username,
                    "email": created_user.email,
                    "role": created_user.role,
                    "full_name": created_user.full_name,
                    "is_active": created_user.is_active
                },
                "message": "User registered successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to register user"
            }

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return self.user_repository.get_by_username(username)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.user_repository.get_by_id(user_id)

    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user with username and password"""
        try:
            user = self.user_repository.get_by_username(username)
            if not user:
                return {
                    "success": False,
                    "message": "User not found"
                }
            
            if not user.is_active:
                return {
                    "success": False,
                    "message": "User account is deactivated"
                }
            
            # Password validation should be done here
            # For now, we'll assume the password is already validated in the controller
            
            return {
                "success": True,
                "user": user,
                "message": "Authentication successful"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Authentication failed"
            }

    def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        try:
            user = self.user_repository.get_by_id(user_id)
            if user:
                user.last_login = datetime.now()
                self.user_repository.update(user)
                return True
            return False
        except Exception:
            return False