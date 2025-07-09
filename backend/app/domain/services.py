"""
Domain services contain business logic that doesn't belong to a specific entity
These are pure business logic functions without external dependencies
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from .models import Vigilante, Building, Shift, ShiftTypeEnum, StatusEnum


class ShiftAssignmentService:
    """Service for intelligent shift assignment logic"""
    
    @staticmethod
    def calculate_shift_hours(shift: Shift) -> Dict[str, float]:
        """Calculate different types of hours for a shift"""
        total_hours = shift.get_duration_hours()
        
        # Business rules for hour calculation
        normal_hours = 0
        overtime_hours = 0
        holiday_hours = 0
        night_hours = 0
        
        # Check if it's a holiday (simplified - you might want to use a holiday calendar)
        is_holiday = shift.start_datetime.weekday() == 6  # Sunday
        
        # Check if it's night shift (between 6 PM and 6 AM)
        start_hour = shift.start_datetime.hour
        end_hour = shift.end_datetime.hour
        is_night_shift = start_hour >= 18 or end_hour <= 6
        
        if is_holiday:
            holiday_hours = total_hours
        elif shift.shift_type == ShiftTypeEnum.OVERTIME:
            overtime_hours = total_hours
        elif is_night_shift:
            night_hours = total_hours
        else:
            normal_hours = total_hours
        
        return {
            "normal_hours": normal_hours,
            "overtime_hours": overtime_hours,
            "holiday_hours": holiday_hours,
            "night_hours": night_hours,
            "total_hours": total_hours
        }
    
    @staticmethod
    def find_best_vigilante_for_shift(
        available_vigilantes: List[Vigilante],
        building: Building,
        shift_datetime: datetime,
        previous_shifts: List[Shift]
    ) -> Optional[Vigilante]:
        """Find the best vigilante for a shift based on business rules"""
        
        if not available_vigilantes:
            return None
        
        # Score each vigilante
        scored_vigilantes = []
        
        for vigilante in available_vigilantes:
            if not vigilante.is_available_for_shift(shift_datetime):
                continue
            
            score = 0
            
            # Check skills match
            building_requirements = set(building.security_requirements)
            vigilante_skills = set(vigilante.skills)
            skill_match = len(building_requirements.intersection(vigilante_skills))
            score += skill_match * 10
            
            # Check rest time (minimum 12 hours between shifts)
            last_shift = ShiftAssignmentService._get_last_shift_for_vigilante(
                vigilante.id, previous_shifts
            )
            if last_shift:
                time_since_last_shift = shift_datetime - last_shift.end_datetime
                if time_since_last_shift >= timedelta(hours=12):
                    score += 5
                else:
                    continue  # Skip if not enough rest
            
            # Prefer vigilantes with fewer recent shifts (load balancing)
            recent_shifts_count = ShiftAssignmentService._count_recent_shifts(
                vigilante.id, previous_shifts, days=7
            )
            score -= recent_shifts_count
            
            scored_vigilantes.append((vigilante, score))
        
        if not scored_vigilantes:
            return None
        
        # Return vigilante with highest score
        scored_vigilantes.sort(key=lambda x: x[1], reverse=True)
        return scored_vigilantes[0][0]
    
    @staticmethod
    def _get_last_shift_for_vigilante(vigilante_id: int, shifts: List[Shift]) -> Optional[Shift]:
        """Get the most recent shift for a vigilante"""
        vigilante_shifts = [s for s in shifts if s.vigilante_id == vigilante_id]
        if not vigilante_shifts:
            return None
        
        return max(vigilante_shifts, key=lambda s: s.end_datetime)
    
    @staticmethod
    def _count_recent_shifts(vigilante_id: int, shifts: List[Shift], days: int = 7) -> int:
        """Count shifts for a vigilante in the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_shifts = [
            s for s in shifts 
            if s.vigilante_id == vigilante_id and s.start_datetime >= cutoff_date
        ]
        return len(recent_shifts)


class PayrollCalculationService:
    """Service for calculating payroll and payments"""
    
    @staticmethod
    def calculate_vigilante_payment(
        vigilante: Vigilante,
        shifts: List[Shift],
        building_rates: Dict[int, Dict[str, float]]
    ) -> Dict[str, Any]:
        """Calculate total payment for a vigilante based on their shifts"""
        
        total_payment = 0
        hours_breakdown = {
            "normal_hours": 0,
            "overtime_hours": 0,
            "holiday_hours": 0,
            "night_hours": 0
        }
        
        for shift in shifts:
            # Get building rates
            building_id = shift.building_id
            rates = building_rates.get(building_id, {})
            
            # Calculate hours for this shift
            shift_hours = ShiftAssignmentService.calculate_shift_hours(shift)
            
            # Calculate payment for each type of hour
            normal_rate = rates.get("hourly_rate", 0)
            overtime_rate = rates.get("overtime_rate", normal_rate * 1.5)
            holiday_rate = rates.get("holiday_rate", normal_rate * 2.0)
            night_rate = normal_rate * 1.25  # 25% night differential
            
            shift_payment = (
                shift_hours["normal_hours"] * normal_rate +
                shift_hours["overtime_hours"] * overtime_rate +
                shift_hours["holiday_hours"] * holiday_rate +
                shift_hours["night_hours"] * night_rate
            )
            
            total_payment += shift_payment
            
            # Accumulate hours
            for hour_type, hours in shift_hours.items():
                if hour_type in hours_breakdown:
                    hours_breakdown[hour_type] += hours
        
        return {
            "vigilante_id": vigilante.id,
            "vigilante_name": vigilante.name,
            "total_payment": total_payment,
            "hours_breakdown": hours_breakdown,
            "total_hours": sum(hours_breakdown.values())
        }


class ContingencyManagementService:
    """Service for handling contingencies like absences and replacements"""
    
    @staticmethod
    def handle_absence(
        absent_vigilante_id: int,
        shift: Shift,
        available_vigilantes: List[Vigilante],
        building: Building,
        previous_shifts: List[Shift]
    ) -> Optional[Vigilante]:
        """Handle vigilante absence by finding a replacement"""
        
        # Filter out the absent vigilante
        replacement_candidates = [
            v for v in available_vigilantes 
            if v.id != absent_vigilante_id
        ]
        
        # Find best replacement using the same logic as normal assignment
        return ShiftAssignmentService.find_best_vigilante_for_shift(
            replacement_candidates,
            building,
            shift.start_datetime,
            previous_shifts
        )
    
    @staticmethod
    def validate_minimum_rest_time(
        vigilante_id: int,
        new_shift: Shift,
        existing_shifts: List[Shift],
        minimum_hours: int = 12
    ) -> bool:
        """Validate that a vigilante has minimum rest time between shifts"""
        
        vigilante_shifts = [s for s in existing_shifts if s.vigilante_id == vigilante_id]
        
        for existing_shift in vigilante_shifts:
            # Check if shifts overlap or are too close
            time_between = abs((new_shift.start_datetime - existing_shift.end_datetime).total_seconds()) / 3600
            
            if time_between < minimum_hours:
                return False
        
        return True
