from flask import Blueprint, request, jsonify
from app.services.profile import ProfileService
from app.models.profile import Profile
from flask_jwt_extended import jwt_required


profile_bp = Blueprint('profiles', __name__)


@profile_bp.route('/user/<int:user_id>', methods=['POST'])
@jwt_required()
def create_profile(user_id):
    try:
        profile_data = request.get_json()
        if not profile_data:
            return jsonify({'error': 'No data provided'}), 400
        profile = ProfileService.create_user_profile(user_id, profile_data)
        return jsonify({
            'message': 'Profile created successfully',
            'profile': profile.serialize()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_profile_by_user_id(user_id):
    try:
        profile = ProfileService.get_user_profile(user_id)
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        return jsonify({
            'profile': profile.serialize()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/<int:profile_id>', methods=['GET'])
@jwt_required()
def get_profile_by_profile_id(profile_id):
    try:
        profile = ProfileService.get_profile_by_profile_id(profile_id)
        if not profile:
            return jsonify({'error': 'Profile not found'}), 404
        return jsonify({
            'profile': profile.serialize()
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_profile_by_user_id(user_id):
    try:
        profile_data = request.get_json()
        if not profile_data:
            return jsonify({'error': 'No data provided'}), 400
        profile = ProfileService.update_user_profile(user_id, profile_data)
        return jsonify({
            'message': 'Profile updated successfully',
            'profile': profile.serialize()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_profile_by_user_id(user_id):
    try:
        success = ProfileService.delete_user_profile(user_id)
        if not success:
            return jsonify({'error': 'Profile not found'}), 404
        return jsonify({
            'message': 'Profile deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500


@profile_bp.route('/user/<int:user_id>/avatar', methods=['PATCH'])
@jwt_required()
def update_avatar(user_id):
    try:
        data = request.get_json()
        if not data or 'avatar_url' not in data:
            return jsonify({'error': 'avatar_url is required'}), 400
        profile = ProfileService.update_avatar(user_id, data['avatar_url'])
        return jsonify({
            'message': 'Avatar updated successfully',
            'profile': profile.serialize()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500