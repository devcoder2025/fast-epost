from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db
from app.models.package import Package
from app.schemas import PackageSchema
from app.utils.validators import validate_request
import logging

bp = Blueprint('packages', __name__)

@bp.route('/add_package', methods=['POST'])
@jwt_required()
@validate_request(PackageSchema)
def add_package():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    try:
        package = Package(
            description=data['description'],
            location=data['location'],
            user_id=user_id,
            status='in_warehouse'
        )
        
        db.session.add(package)
        db.session.commit()
        
        return jsonify({
            'message': 'Package added successfully',
            'package_id': package.id
        }), 201
    except Exception as e:
        logging.error(f"Error adding package: {e}")
        return jsonify({'message': 'Error adding package'}), 500

@bp.route('/packages', methods=['GET'])
@jwt_required()
def get_packages():
    user_id = get_jwt_identity()
    packages = Package.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'packages': [{
            'id': p.id,
            'description': p.description,
            'status': p.status,
            'location': p.location,
            'timestamp': p.timestamp.isoformat()
        } for p in packages]
    })

@bp.route('/package/<int:package_id>/status', methods=['PUT'])
@jwt_required()
def update_status(package_id):
    data = request.get_json()
    package = Package.query.get_or_404(package_id)
    
    try:
        package.status = data['status']
        package.location = data.get('location', package.location)
        
        history = PackageHistory(
            status=data['status'],
            location=data.get('location'),
            notes=data.get('notes')
        )
        package.history.append(history)
        
        db.session.commit()
        
        return jsonify({'message': 'Package status updated successfully'})
    except Exception as e:
        logging.error(f"Error updating package status: {e}")
        return jsonify({'message': 'Error updating package status'}), 500
