from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.steam_service import SteamService
from app.services.library import LibraryService
from app.services.admin import AdminService
import logging

logger = logging.getLogger(__name__)
cart_controller = Blueprint('cart', __name__, url_prefix='/api/cart')

# Dictionary to simulate a database for cart items
# In a real application, this would be stored in a database
# Structure: {user_id: [steam_game_id1, steam_game_id2, ...]}
cart_data = {}

@cart_controller.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get items in user's cart with Steam game details"""
    try:
        current_user_id = get_jwt_identity()
        
        # Convert to int if needed (JWT identity might be string)
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        # Get user's cart items (Steam game IDs)
        steam_game_ids = cart_data.get(str(current_user_id), [])
        
        # Get Steam game details for each item
        steam_service = SteamService()
        cart_items = []
        
        for steam_game_id in steam_game_ids:
            game_details = steam_service.get_game_details(steam_game_id)
            if game_details:
                cart_items.append(game_details)
        
        return jsonify({
            "success": True,
            "message": "Cart retrieved successfully",
            "data": cart_items
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in get_cart: {e}")
        return jsonify({"success": False, "message": "Failed to fetch cart"}), 500

@cart_controller.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add a game to the user's cart"""
    try:
        current_user_id = get_jwt_identity()
        
        # Convert to int if needed (JWT identity might be string)
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        data = request.get_json()
        
        if 'steam_game_id' not in data:
            return jsonify({"success": False, "message": "Missing steam_game_id parameter"}), 400
        
        steam_game_id = data['steam_game_id']
        
        # Validate game exists on Steam
        steam_service = SteamService()
        game_details = steam_service.get_game_details(steam_game_id)
        if not game_details:
            return jsonify({"success": False, "message": "Game not found on Steam"}), 404
        
        user_id_str = str(current_user_id)
        
        # Initialize user's cart if it doesn't exist
        if user_id_str not in cart_data:
            cart_data[user_id_str] = []
            
        # Check if game is already in cart
        if steam_game_id in cart_data[user_id_str]:
            return jsonify({"success": False, "message": "Game already in cart"}), 409
            
        # Add game to cart
        cart_data[user_id_str].append(steam_game_id)
        
        return jsonify({
            "success": True,
            "message": "Game added to cart successfully",
            "data": {
                "steam_game_id": steam_game_id,
                "game": game_details
            }
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error in add_to_cart: {e}")
        return jsonify({"success": False, "message": "Failed to add to cart"}), 500

@cart_controller.route('/remove/<int:steam_game_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(steam_game_id):
    """Remove a game from the user's cart"""
    try:
        current_user_id = get_jwt_identity()
        
        # Convert to int if needed (JWT identity might be string)
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        user_id_str = str(current_user_id)
        
        # Check if user has a cart
        if user_id_str not in cart_data:
            return jsonify({"success": False, "message": "Cart not found"}), 404
            
        # Check if game is in cart
        if steam_game_id not in cart_data[user_id_str]:
            return jsonify({"success": False, "message": "Game not in cart"}), 404
            
        # Remove game from cart
        cart_data[user_id_str].remove(steam_game_id)
        
        return jsonify({
            "success": True,
            "message": "Game removed from cart successfully"
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in remove_from_cart: {e}")
        return jsonify({"success": False, "message": "Failed to remove game from cart"}), 500

@cart_controller.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from the user's cart"""
    try:
        current_user_id = get_jwt_identity()
        
        # Convert to int if needed (JWT identity might be string)
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        user_id_str = str(current_user_id)
        
        # Check if user has a cart
        if user_id_str not in cart_data:
            return jsonify({"success": True, "message": "Cart already empty"}), 200
            
        # Clear cart
        cart_data[user_id_str] = []
        
        return jsonify({"success": True, "message": "Cart cleared successfully"}), 200
        
    except Exception as e:
        current_app.logger.error(f"Error in clear_cart: {e}")
        return jsonify({"success": False, "message": "Failed to clear cart"}), 500

@cart_controller.route('/purchase', methods=['POST'])
@jwt_required()
def purchase_cart():
    """Purchase all items in cart and add them to user's library"""
    try:
        current_user_id = get_jwt_identity()
        
        # Convert to int if needed (JWT identity might be string)
        if isinstance(current_user_id, str):
            current_user_id = int(current_user_id)
        
        user_id_str = str(current_user_id)
        
        # Check if user has a cart
        if user_id_str not in cart_data or not cart_data[user_id_str]:
            return jsonify({"success": False, "message": "Cart is empty"}), 400
        
        steam_game_ids = cart_data[user_id_str].copy()
        purchased_games = []
        failed_games = []
        
        # Try to add each game to library
        for steam_game_id in steam_game_ids:
            try:
                # Add game to library
                library_item = LibraryService.add_to_library(current_user_id, steam_game_id)
                
                # Get game details for response
                steam_service = SteamService()
                game_details = steam_service.get_game_details(steam_game_id)
                
                purchased_games.append({
                    "library_id": library_item.id,
                    "steam_game_id": steam_game_id,
                    "added_at": library_item.added_at,
                    "game": game_details
                })
                
            except Exception as e:
                current_app.logger.error(f"Failed to add game {steam_game_id} to library: {e}")
                failed_games.append({
                    "steam_game_id": steam_game_id,
                    "error": str(e)
                })
        
        # Clear cart on successful purchase (even if some games failed)
        if purchased_games:
            cart_data[user_id_str] = []
        
        # Prepare response
        response_data = {
            "purchased_games": purchased_games,
            "total_purchased": len(purchased_games),
            "total_failed": len(failed_games)
        }
        
        if failed_games:
            response_data["failed_games"] = failed_games
        
        if purchased_games and not failed_games:
            return jsonify({
                "success": True,
                "message": f"Successfully purchased {len(purchased_games)} games",
                "data": response_data
            }), 200
        elif purchased_games and failed_games:
            return jsonify({
                "success": True,
                "message": f"Purchased {len(purchased_games)} games, {len(failed_games)} failed",
                "data": response_data
            }), 207  # Multi-status
        else:
            return jsonify({
                "success": False,
                "message": "Failed to purchase any games",
                "data": response_data
            }), 400
            
    except Exception as e:
        current_app.logger.error(f"Error in purchase_cart: {e}")
        return jsonify({"success": False, "message": "Failed to process purchase"}), 500
