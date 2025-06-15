from app.repositories.library import LibraryRepository
from app.models.game import Game
from app.models.user import User
from app.extensions import db
from sqlalchemy import select
from typing import List, Optional, Dict, Any

class LibraryService:
    @staticmethod
    def get_user_library(user_id: int):
        return LibraryRepository.get_user_library(user_id)
    
    @staticmethod
    def get_library_item(user_id: int, game_id: int):
        return LibraryRepository.get_library_item(user_id, game_id)
    
    @staticmethod
    def add_to_library(user_id: int, game_id: int):
        stmt = select(Game).where(Game.id == game_id)
        game = db.session.execute(stmt).scalar_one_or_none()
        if not game:
            raise ValueError("Game not found")
        
        stmt = select(User).where(User.id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        if not user:
            raise ValueError("User not found")
        
        return LibraryRepository.add_to_library(user_id, game_id)
    
    @staticmethod
    def remove_from_library(user_id: int, game_id: int):
        return LibraryRepository.remove_from_library(user_id, game_id)
    
    @staticmethod
    def format_library_response(library_items):
        formatted_items = []
        for item in library_items:
            formatted_items.append({
                "library_id": item.id,
                "added_at": item.added_at,
                "game": item.game.serialize() if item.game else None
            })
        return formatted_items
