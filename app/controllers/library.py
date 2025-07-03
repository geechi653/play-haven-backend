from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from sqlalchemy import select
from app.services.library import LibraryService
from app.services.admin import AdminService
import logging

library_bp = Blueprint('library', __name__)


@library_bp.route('/user/<int:user_id>/library', methods=['GET'])
@jwt_required()
def get_user_library(user_id):
    current_user_id = get_jwt_identity()

    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)

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


@library_bp.route('/user/<int:user_id>/library/game/<int:steam_game_id>', methods=['GET'])
@jwt_required()
def get_library_game(user_id, steam_game_id):
    current_user_id = get_jwt_identity()

    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)

    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403

    try:
        library_item = LibraryService.get_library_item(user_id, steam_game_id)

        if not library_item:
            return jsonify({"success": False, "message": "Game not found in user's library"}), 404

        return jsonify({
            "success": True,
            "message": "Game retrieved successfully",
            "data": {
                "library_id": library_item.id,
                "added_at": library_item.added_at,
                "steam_game_id": library_item.steam_game_id
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving library game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to retrieve library game"}), 500


@library_bp.route('/user/<int:user_id>/library/game/<int:steam_game_id>', methods=['DELETE'])
@jwt_required()
def remove_library_game(user_id, steam_game_id):
    current_user_id = get_jwt_identity()

    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)

    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403

    try:
        success = LibraryService.remove_from_library(user_id, steam_game_id)

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

    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)

    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403

    data = request.get_json()

    if 'steam_game_id' not in data:
        return jsonify({"success": False, "message": "Missing steam_game_id parameter"}), 400

    steam_game_id = data['steam_game_id']

    try:
        try:
            library_item = LibraryService.add_to_library(user_id, steam_game_id)
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)}), 404

        return jsonify({
            "success": True,
            "message": "Game added to library successfully",
            "data": {
                "library_id": library_item.id,
                "added_at": library_item.added_at,
                "steam_game_id": library_item.steam_game_id
            }
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error adding game to library: {str(e)}")
        return jsonify({"success": False, "message": "Failed to add game to library"}), 500
