from flask import Blueprint, jsonify, request, current_app
import logging
from functools import wraps

logger = logging.getLogger(__name__)
cart_controller = Blueprint('cart', __name__, url_prefix='/api/cart')

# Dictionary to simulate a database for cart items
# In a real application, this would be stored in a database
cart_data = {}

def login_required(f):
    """Decorator to check if the user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = request.args.get('userId') or (request.json and request.json.get('userId'))
        
        if not user_id:
            return jsonify({"error": "Authentication required", "redirect": "/login"}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@cart_controller.route('', methods=['GET'])
@login_required
def get_cart():
    """Get items in user's cart"""
    try:
        user_id = request.args.get('userId')
        
        # Return cart for the user (or empty list if user has no cart)
        user_cart = cart_data.get(user_id, [])
        return jsonify(user_cart)
    except Exception as e:
        logger.error(f"Error in get_cart: {e}")
        return jsonify({"error": "Failed to fetch cart"}), 500

@cart_controller.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    """Add a game to the user's cart"""
    try:
        data = request.json
        user_id = data.get('userId')
        game_id = data.get('gameId')
        
        if not user_id or not game_id:
            return jsonify({"error": "User ID and Game ID are required"}), 400
            
        # Initialize user's cart if it doesn't exist
        if user_id not in cart_data:
            cart_data[user_id] = []
            
        # Check if game is already in cart
        if game_id in cart_data[user_id]:
            return jsonify({"message": "Game already in cart"}), 200
            
        # Add game to cart
        cart_data[user_id].append(game_id)
        
        return jsonify({"message": "Game added to cart", "cartItems": cart_data[user_id]}), 201
    except Exception as e:
        logger.error(f"Error in add_to_cart: {e}")
        return jsonify({"error": "Failed to add game to cart"}), 500

@cart_controller.route('/remove/<int:game_id>', methods=['DELETE'])
@login_required
def remove_from_cart(game_id):
    """Remove a game from the user's cart"""
    try:
        user_id = request.args.get('userId')
        
        # Check if user has a cart
        if user_id not in cart_data:
            return jsonify({"error": "Cart not found"}), 404
            
        # Check if game is in cart
        if game_id not in cart_data[user_id]:
            return jsonify({"error": "Game not in cart"}), 404
            
        # Remove game from cart
        cart_data[user_id].remove(game_id)
        
        return jsonify({"message": "Game removed from cart", "cartItems": cart_data[user_id]}), 200
    except Exception as e:
        logger.error(f"Error in remove_from_cart: {e}")
        return jsonify({"error": "Failed to remove game from cart"}), 500

@cart_controller.route('/clear', methods=['DELETE'])
@login_required
def clear_cart():
    """Clear all items from the user's cart"""
    try:
        user_id = request.args.get('userId')
        
        # Check if user has a cart
        if user_id not in cart_data:
            return jsonify({"message": "Cart already empty"}), 200
            
        # Clear cart
        cart_data[user_id] = []
        
        return jsonify({"message": "Cart cleared"}), 200
    except Exception as e:
        logger.error(f"Error in clear_cart: {e}")
        return jsonify({"error": "Failed to clear cart"}), 500
