from flask import Blueprint, jsonify, current_app, request
from app.services.steam_service import SteamService
import logging
import datetime
import random

logger = logging.getLogger(__name__)
steam_controller = Blueprint('steam', __name__, url_prefix='/api/steam')

@steam_controller.route('/top-games', methods=['GET'])
def get_top_games():
    """Get top most played games"""
    try:
        # Get limit and offset parameters from query string or use default
        limit = request.args.get('limit', default=10, type=int)
        limit = min(limit, 50)  # Cap at 50 to prevent abuse
        offset = request.args.get('offset', default=0, type=int)
        offset = max(offset, 0)
        
        steam_service = SteamService()
        games = steam_service.get_top_games(limit, offset)
        return jsonify(games)
    except Exception as e:
        logger.error(f"Error in get_top_games: {e}")
        return jsonify({"error": "Failed to fetch top games"}), 500

@steam_controller.route('/discounted-games', methods=['GET'])
def get_discounted_games():
    """Get discounted games"""
    try:
        # Get limit parameter from query string or use default
        limit = request.args.get('limit', default=10, type=int)
        limit = min(limit, 30)  # Cap at 30 to prevent abuse
        
        steam_service = SteamService()
        games = steam_service.get_discounted_games(limit)
        return jsonify(games)
    except Exception as e:
        logger.error(f"Error in get_discounted_games: {e}")
        return jsonify({"error": "Failed to fetch discounted games"}), 500

@steam_controller.route('/featured-games', methods=['GET'])
def get_featured_games():
    """Get featured games"""
    try:
        # Get limit parameter from query string or use default
        limit = request.args.get('limit', default=10, type=int)
        limit = min(limit, 30)  # Cap at 30 to prevent abuse
        
        steam_service = SteamService()
        games = steam_service.get_featured_games(limit)
        return jsonify(games)
    except Exception as e:
        logger.error(f"Error in get_featured_games: {e}")
        return jsonify({"error": "Failed to fetch featured games"}), 500

@steam_controller.route('/games/<int:app_id>', methods=['GET'])
def get_game_details(app_id):
    """Get detailed information for a specific game"""
    try:
        steam_service = SteamService()
        game = steam_service.get_game_details(app_id)
        if game:
            return jsonify(game)
        return jsonify({"error": "Game not found"}), 404
    except Exception as e:
        logger.error(f"Error in get_game_details for app_id {app_id}: {e}")
        return jsonify({"error": "Failed to fetch game details"}), 500

@steam_controller.route('/search', methods=['GET'])
def search_games():
    """Search for games by name"""
    try:
        # Get query parameter
        query = request.args.get('q', default='', type=str)
        if not query or len(query) < 3:
            return jsonify({"error": "Search query must be at least 3 characters"}), 400
            
        # Get limit parameter
        limit = request.args.get('limit', default=20, type=int)
        limit = min(limit, 50)  # Cap at 50 to prevent abuse
        
        steam_service = SteamService()
        games = steam_service.search_games(query, limit)
        return jsonify(games)
    except Exception as e:
        logger.error(f"Error in search_games with query '{query}': {e}")
        return jsonify({"error": "Failed to search games"}), 500

@steam_controller.route('/download/<int:app_id>', methods=['GET'])
def download_game(app_id):
    """Handle game download requests with authentication"""
    try:
        # Check for user authentication
        user_id = request.args.get('userId')
        if not user_id:
            return jsonify({"error": "Authentication required", "redirect": "/login"}), 401
            
        # In a real app, we would check if the user owns the game
        # For now, we'll just return game info for download
        steam_service = SteamService()
        game = steam_service.get_game_details(app_id)
        
        if not game:
            return jsonify({"error": "Game not found"}), 404
            
        # Add download info to the game data
        game['download_info'] = {
            'download_id': f"dl-{app_id}-{user_id}",
            'timestamp': str(datetime.datetime.now()),
            'size': f"{random.randint(1, 50)} GB",
            'estimated_time': f"{random.randint(10, 120)} minutes",
        }
        
        return jsonify(game)
    except Exception as e:
        logger.error(f"Error in download_game for app_id {app_id}: {e}")
        return jsonify({"error": "Failed to prepare game for download"}), 500
