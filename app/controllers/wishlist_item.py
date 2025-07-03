from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin import AdminService
from app.services.wishlist_item import WishlistService

wishlist_item_bp = Blueprint("wishlist", __name__)

@wishlist_item_bp.route('', methods=['GET'])
@jwt_required()
def get_wishlist():
    """Get current user's wishlist"""
    current_user_id = get_jwt_identity()
    
    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)
    
    try:
        wishlist_items = WishlistService.get_user_wishlist(current_user_id)
        games = WishlistService.format_wishlist_response(wishlist_items)

        return jsonify({
            "success": True,
            "message": "Wishlist retrieved successfully",
            "data": games
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving wishlist: {str(e)}")
        return jsonify({"success": False, "message": "Failed to retrieve wishlist"}), 500

@wishlist_item_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    """Add game to current user's wishlist"""
    current_user_id = get_jwt_identity()
    
    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)

    data = request.get_json()

    if 'steam_game_id' not in data:
        return jsonify({"success": False, "message": "Missing steam_game_id parameter"}), 400

    steam_game_id = data['steam_game_id']

    try:
        try:
            wishlist_item = WishlistService.add_to_wishlist(current_user_id, steam_game_id)
        except ValueError as e:
            if "already in wishlist" in str(e).lower():
                return jsonify({"success": False, "message": "Game already in wishlist"}), 409
            return jsonify({"success": False, "message": str(e)}), 404

        return jsonify({
            "success": True,
            "message": "Game added to wishlist successfully",
            "data": {
                "wishlist_id": wishlist_item.id,
                "created_at": wishlist_item.created_at,
                "steam_game_id": wishlist_item.steam_game_id
            }
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error adding game to wishlist: {str(e)}")
        return jsonify({"success": False, "message": "Failed to add game to wishlist"}), 500

@wishlist_item_bp.route('/remove/<int:steam_game_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(steam_game_id):
    """Remove game from current user's wishlist"""
    current_user_id = get_jwt_identity()

    # Convert to int if needed (JWT identity might be string)
    if isinstance(current_user_id, str):
        current_user_id = int(current_user_id)

    try:
        success = WishlistService.delete_from_wishlist(current_user_id, steam_game_id)

        if not success:
            return jsonify({"success": False, "message": "Game not found in wishlist"}), 404

        return jsonify({
            "success": True,
            "message": "Game removed from wishlist successfully"
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error removing wishlist game: {str(e)}")
        return jsonify({"success": False, "message": "Failed to remove game from wishlist"}), 500

# Admin endpoints for accessing other users' wishlists
@wishlist_item_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_wishlist(user_id):
    """Get specific user's wishlist (admin only)"""
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