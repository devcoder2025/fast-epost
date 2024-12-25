from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.vat_service import VatService
from app.services.route_service import RouteService

bp = Blueprint('services', __name__)

@bp.route('/calculate-vat', methods=['POST'])
@jwt_required()
def calculate_vat():
    data = request.get_json()
    amount = float(data['amount'])
    
    try:
        result = VatService.calculate_vat(amount)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/optimize-route', methods=['POST'])
@jwt_required()
def optimize_route():
    data = request.get_json()
    origin = data['origin']
    destinations = data['destinations']
    
    try:
        result = RouteService.optimize_route(origin, destinations)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
