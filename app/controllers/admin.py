from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from sqlalchemy import select
from app.services.admin import AdminService
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def is_admin():
    current_user_id = get_jwt_identity()
    return AdminService.is_admin(current_user_id)

@admin_bp.route('/games', methods=['POST'])
@jwt_required()
def add_game():
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    data = request.get_json()
    
    try:
        new_game = AdminService.create_game(data)
        return jsonify({"success": True, "message": "Game added successfully", "data": new_game.serialize()}), 201
    
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error adding game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to add game"}), 500

@admin_bp.route('/games/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    data = request.get_json()
    
    try:
        game = AdminService.update_game(game_id, data)
        
        if not game:
            return jsonify({"success": False, "message": "Game not found"}), 404
        
        return jsonify({"success": True, "message": "Game updated successfully", "data": game.serialize()}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error updating game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update game"}), 500

@admin_bp.route('/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    try:
        success = AdminService.delete_game(game_id)
        
        if not success:
            return jsonify({"success": False, "message": "Game not found"}), 404
        
        return jsonify({"success": True, "message": "Game deleted successfully"}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error deleting game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete game"}), 500

@admin_bp.route('/fetch-game-data', methods=['POST'])
@jwt_required()
def fetch_game_data():
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    data = request.get_json()
    
    if 'app_id' not in data:
        return jsonify({"success": False, "message": "Missing app_id parameter"}), 400
    
    app_id = data['app_id']
    
    try:
        game_data = AdminService.fetch_game_data_from_steam(app_id)
        
        if not game_data:
            return jsonify({"success": False, "message": "Game not found or not supported"}), 404
        
        return jsonify({"success": True, "data": game_data}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error fetching game data: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch game data"}), 500

@admin_bp.route('/games/<int:game_id>', methods=['PUT'])
@jwt_required()
def update_game(game_id):
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    data = request.get_json()
    
    try:
        game = AdminService.update_game(game_id, data)
        
        if not game:
            return jsonify({"success": False, "message": "Game not found"}), 404
        
        return jsonify({"success": True, "message": "Game updated successfully", "data": game.serialize()}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error updating game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to update game"}), 500

@admin_bp.route('/games/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_game(game_id):
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    try:
        success = AdminService.delete_game(game_id)
        
        if not success:
            return jsonify({"success": False, "message": "Game not found"}), 404
        
        return jsonify({"success": True, "message": "Game deleted successfully"}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error deleting game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to delete game"}), 500

@admin_bp.route('/fetch-game-data', methods=['POST'])
@jwt_required()
def fetch_game_data():
    if not is_admin():
        return jsonify({"success": False, "message": "Admin access required"}), 403
    
    data = request.get_json()
    
    if 'app_id' not in data:
        return jsonify({"success": False, "message": "Missing app_id parameter"}), 400
    
    app_id = data['app_id']
    
    try:
        game_data = AdminService.fetch_game_data_from_steam(app_id)
        
        if not game_data:
            return jsonify({"success": False, "message": "Game not found or not supported"}), 404
        
        return jsonify({"success": True, "data": game_data}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error fetching game data: {str(e)}")
        return jsonify({"success": False, "message": "Failed to fetch game data"}), 500
