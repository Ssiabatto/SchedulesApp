"""
API Routes - Interface Layer
This layer handles HTTP requests and responses
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from typing import Dict, Any

import os
from ...application.services import VigilanteService, BuildingService, ShiftService, ReportService
from ...infrastructure.database import (
    DatabaseSession, 
    SQLVigilanteRepository, 
    SQLBuildingRepository, 
    SQLShiftRepository, 
    SQLReportRepository
)

# Create blueprints
api_bp = Blueprint('api', __name__, url_prefix='/api')
vigilantes_bp = Blueprint('vigilantes', __name__, url_prefix='/api/vigilantes')
shifts_bp = Blueprint('shifts', __name__, url_prefix='/api/shifts')
buildings_bp = Blueprint('buildings', __name__, url_prefix='/api/buildings')
reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

# Initialize database session from environment or default
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/gestion_turnos_vigilantes')
db_session_manager = DatabaseSession(DATABASE_URL)
db_session = db_session_manager.get_session()

# Initialize repositories
vigilante_repository = SQLVigilanteRepository(db_session)
building_repository = SQLBuildingRepository(db_session)
shift_repository = SQLShiftRepository(db_session)
report_repository = SQLReportRepository(db_session)

# Initialize services
vigilante_service = VigilanteService(vigilante_repository)
building_service = BuildingService(building_repository)
shift_service = ShiftService(shift_repository, vigilante_repository, building_repository)
report_service = ReportService(report_repository, shift_repository, vigilante_repository, building_repository)


# Error handlers
@api_bp.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "message": "Bad request", "error": str(error)}), 400

@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "message": "Resource not found"}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "message": "Internal server error"}), 500


# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running"""
    return jsonify({
        "success": True,
        "message": "API is running",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }), 200


# Vigilantes endpoints
@vigilantes_bp.route('/', methods=['GET'])
@jwt_required()
def get_vigilantes():
    """Get all vigilantes"""
    try:
        filters = request.args.to_dict()
        result = vigilante_service.get_all_vigilantes(filters)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@vigilantes_bp.route('/', methods=['POST'])
@jwt_required()
def create_vigilante():
    """Create a new vigilante"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        result = vigilante_service.register_vigilante(data)
        
        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@vigilantes_bp.route('/<int:vigilante_id>', methods=['GET'])
@jwt_required()
def get_vigilante(vigilante_id):
    """Get vigilante by ID"""
    try:
        result = vigilante_service.get_vigilante(vigilante_id)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Buildings endpoints
@buildings_bp.route('/', methods=['GET'])
@jwt_required()
def get_buildings():
    """Get all buildings"""
    try:
        result = building_service.get_all_buildings()
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@buildings_bp.route('/', methods=['POST'])
@jwt_required()
def create_building():
    """Create a new building"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        result = building_service.create_building(data)
        
        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Shifts endpoints
@shifts_bp.route('/', methods=['GET'])
@jwt_required()
def get_shifts():
    """Get all shifts"""
    try:
        filters = request.args.to_dict()
        result = shift_service.get_all_shifts(filters)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@shifts_bp.route('/', methods=['POST'])
@jwt_required()
def create_shift():
    """Create a new shift"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        result = shift_service.create_shift(data)
        
        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@shifts_bp.route('/<int:shift_id>', methods=['GET'])
@jwt_required()
def get_shift(shift_id):
    """Get shift by ID"""
    try:
        result = shift_service.get_shift(shift_id)
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Reports endpoints
@reports_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_report():
    """Generate a report"""
    try:
        criteria = request.get_json()
        if not criteria:
            return jsonify({"success": False, "message": "No criteria provided"}), 400
        
        result = report_service.generate_report(criteria)
        
        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@reports_bp.route('/<int:report_id>/export/<string:format>', methods=['POST'])
@jwt_required()
def export_report(report_id, format):
    """Export report in specified format"""
    try:
        result = report_service.export_report(report_id, format.lower())
        
        if result["success"]:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Register all blueprints
def register_routes(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(api_bp)
    app.register_blueprint(vigilantes_bp)
    app.register_blueprint(buildings_bp)
    app.register_blueprint(shifts_bp)
    app.register_blueprint(reports_bp)