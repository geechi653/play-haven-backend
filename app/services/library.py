from app.repositories.library import LibraryRepository
from app.models.user import User
from app.extensions import db
from app.services.steam_service import SteamService
from sqlalchemy import select
from typing import List, Optional, Dict, Any

class LibraryService:
    @staticmethod
    def get_user_library(user_id: int):
        return LibraryRepository.get_user_library(user_id)
    
    @staticmethod
    def get_library_item(user_id: int, steam_game_id: int):
        return LibraryRepository.get_library_item(user_id, steam_game_id)
    
    @staticmethod
    def add_to_library(user_id: int, steam_game_id: int):
        # Validate user exists
        stmt = select(User).where(User.id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        if not user:
            raise ValueError("User not found")
        
        # Validate game exists on Steam
        steam_service = SteamService()
        game_details = steam_service.get_game_details(steam_game_id)
        if not game_details:
            raise ValueError("Game not found on Steam")
        
        return LibraryRepository.add_to_library(user_id, steam_game_id)
    
    @staticmethod
    def remove_from_library(user_id: int, steam_game_id: int):
        return LibraryRepository.remove_from_library(user_id, steam_game_id)
    
    @staticmethod
    def format_library_response(library_items):
        steam_service = SteamService()
        formatted_items = []
        for item in library_items:
            # Get game details from Steam API
            game_details = steam_service.get_game_details(item.steam_game_id)
            formatted_items.append({
                "library_id": item.id,
                "added_at": item.added_at,
                "game": game_details  # Steam game details
            })
        return formatted_items
