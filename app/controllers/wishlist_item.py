from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin import AdminService
from app.services.wishlist_item import WishlistService

wishlist_item_bp = Blueprint("wishlist_items", __name__)

@wishlist_item_bp.route('/user/<int:user_id>/wishlist', methods=['GET'])
@jwt_required()
def get_user_wishlist(user_id):
    current_user_id = get_jwt_identity()
    
    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access to the wishlist denied"}), 403
    try:
        wishlist_items = WishlistService.get_user_wishlist(user_id)
        games = WishlistService.format_wishlist_response(wishlist_items)
        return jsonify({"success": True, "message": "User wishlist retrieved successfully", "data": games}), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving user wishlist: {str(e)}")
        return jsonify({"success": False, "message": "Failed to retrieve user wishlist"}), 500
    

@wishlist_item_bp.route('/user/<int:user_id>/wishlist/add', methods=['POST'])
@jwt_required()
def add_wishlist_item(user_id):
    current_user_id = get_jwt_identity()
    
    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access denied"}), 403
    data = request.get_json()
    if 'game_id' not in data:
        return jsonify({"success": False, "message": "Missing game_id parameter"}), 400
    game_id = data['game_id']
    try:
        try:
            wishlist_item = WishlistService.add_to_wishlist(user_id, game_id)
        except ValueError as e:
            return jsonify({"success": False, "message": str(e)}), 404
        return jsonify({"success": True, "message": "Game added to wishlist successfully",
            "data": {
                "wishlist_id": wishlist_item.id,
                "created_at": wishlist_item.created_at,
                "game": wishlist_item.game.serialize() if wishlist_item.game else None
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f"Error adding game to wishlist: {str(e)}")
        return jsonify({"success": False, "message": "Failed to add game to wishlist"}), 500


@wishlist_item_bp.route('/user/<int:user_id>/wishlist/game/<int:game_id>', methods=['DELETE'])
@jwt_required()
def delete_item_from_wishlist(user_id, game_id):
    current_user_id = get_jwt_identity()
    
    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    if current_user_id != user_id and not AdminService.is_admin(current_user_id):
        return jsonify({"success": False, "message": "Access to wishlist denied"}), 403
    try:
        success = WishlistService.delete_from_wishlist(user_id, game_id)
        if not success:
            return jsonify({"success": False, "message": "Game not found in user's wishlist"}), 404
        return jsonify({"success": True, "message": "Game removed from wishlist successfully"}), 200
    
    except Exception as e:
        current_app.logger.error(f"Error removing wishlist game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to remove game from wishlist"}), 500