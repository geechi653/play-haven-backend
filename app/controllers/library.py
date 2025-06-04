from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from sqlalchemy import select
from app.services.library import LibraryService
from app.services.admin import AdminService
import logging

library_bp = Blueprint('library', __name__, url_prefix='/api')

@library_bp.route('/user/<int:user_id>/library', methods=['GET'])
@jwt_required()
def get_user_library(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        library_items = LibraryService.get_user_library(user_id)
        games = LibraryService.format_library_response(library_items)
        
        return jsonify({
            "success": True, 
            "message": "User library retrieved successfully", 
            "data": games
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving user library: {str(e)}")
        return jsonify({"success": False, "message": "Failed to retrieve user library"}), 500

@library_bp.route('/user/<int:user_id>/library/game/<int:game_id>', methods=['GET'])
@jwt_required()
def get_library_game(user_id, game_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        library_item = LibraryService.get_library_item(user_id, game_id)
        
        if not library_item:
            return jsonify({"success": False, "message": "Game not found in user's library"}), 404
        
        return jsonify({
            "success": True, 
            "message": "Game retrieved successfully", 
            "data": {
                "library_id": library_item.id,
                "added_at": library_item.added_at,
                "game": library_item.user_games.serialize() if library_item.user_games else None
            }
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving library game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to retrieve library game"}), 500

@library_bp.route('/user/<int:user_id>/library/game/<int:game_id>', methods=['DELETE'])
@jwt_required()
def remove_library_game(user_id, game_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        success = LibraryService.remove_from_library(user_id, game_id)
        
        if not success:
            return jsonify({"success": False, "message": "Game not found in user's library"}), 404
        
        return jsonify({
            "success": True, 
            "message": "Game removed from library successfully"
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error removing library game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to remove game from library"}), 500

@library_bp.route('/user/<int:user_id>/library/add', methods=['POST'])
@jwt_required()
def add_to_library(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    data = request.get_json()
    
    if 'game_id' not in data:
        return jsonify({"success": False, "message": "Missing game_id parameter"}), 400
    
    game_id = data['game_id']
    
    try:
        try:
            library_item = LibraryService.add_to_library(user_id, game_id)
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)}), 404
        
        return jsonify({
            "success": True, 
            "message": "Game added to library successfully",
            "data": {
                "library_id": library_item.id,
                "added_at": library_item.added_at,
                "game": library_item.user_games.serialize() if library_item.user_games else None
            }
        }), 201
    
    except Exception as e:
        current_app.logger.error(f"Error adding game to library: {str(e)}")
        return jsonify({"success": False, "message": "Failed to add game to library"}), 500

@library_bp.route('/<int:user_id>/library/game/<int:game_id>', methods=['GET'])
@jwt_required()
def get_library_game(user_id, game_id):
    current_user_id = get_jwt_identity()
    
    # Check if the user is requesting their own library or is an admin
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        # Get the specific game from the user's library
        library_item = LibraryService.get_library_item(user_id, game_id)
        
        if not library_item:
            return jsonify({"success": False, "message": "Game not found in user's library"}), 404
        
        return jsonify({
            "success": True, 
            "message": "Game retrieved successfully", 
            "data": {
                "library_id": library_item.id,
                "added_at": library_item.added_at,
                "game": library_item.user_games.serialize() if library_item.user_games else None
            }
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error retrieving library game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to retrieve library game"}), 500

@library_bp.route('/<int:user_id>/library/game/<int:game_id>', methods=['DELETE'])
@jwt_required()
def remove_library_game(user_id, game_id):
    current_user_id = get_jwt_identity()
    
    # Check if the user is removing from their own library or is an admin
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    try:
        # Remove the game from the library
        success = LibraryService.remove_from_library(user_id, game_id)
        
        if not success:
            return jsonify({"success": False, "message": "Game not found in user's library"}), 404
        
        return jsonify({
            "success": True, 
            "message": "Game removed from library successfully"
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Error removing library game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to remove game from library"}), 500

# This endpoint could be used when a user completes a purchase to add a game to their library
@library_bp.route('/<int:user_id>/library/add', methods=['POST'])
@jwt_required()
def add_to_library(user_id):
    current_user_id = get_jwt_identity()
    
    # Check if the user is adding to their own library or is an admin
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    
    data = request.get_json()
    
    if 'game_id' not in data:
        return jsonify({"success": False, "message": "Missing game_id parameter"}), 400
    
    game_id = data['game_id']
    
    try:
        # Add the game to the library
        try:
            library_item = LibraryService.add_to_library(user_id, game_id)
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)}), 404
        
        return jsonify({
            "success": True, 
            "message": "Game added to library successfully",
            "data": {
                "library_id": library_item.id,
                "added_at": library_item.added_at,
                "game": library_item.user_games.serialize() if library_item.user_games else None
            }
        }), 201
    
    except Exception as e:
        current_app.logger.error(f"Error adding game to library: {str(e)}")
        return jsonify({"success": False, "message": "Failed to add game to library"}), 500
