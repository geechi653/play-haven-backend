from app.repositories.wishlist_item import WishlistItemRepository
from app.models.game import Game
from app.models.user import User
from app.extensions import db
from sqlalchemy import select
from typing import List, Optional, Dict, Any

class WishlistService:
    @staticmethod
    def get_user_wishlist(user_id: int):
        return WishlistItemRepository.get_user_wishlist(user_id)
    
    @staticmethod
    def get_wishlist_item(user_id: int, game_id: int):
        return WishlistItemRepository.get_wishlist_item(user_id, game_id)
    
    @staticmethod
    def add_to_wishlist(user_id: int, game_id: int):
        stmt = select(Game).where(Game.id == game_id)
        game = db.session.execute(stmt).scalar_one_or_none()
        if not game:
            raise ValueError("Game not found")
        
        stmt = select(User).where(User.id == user_id)
        user = db.session.execute(stmt).scalar_one_or_none()
        if not user:
            raise ValueError("User not found")
        
        return WishlistItemRepository.add_to_wishlist(user_id, game_id)
    
    @staticmethod
    def delete_from_wishlist(user_id: int, game_id: int):
        return WishlistItemRepository.delete_from_wishlist(user_id, game_id)
    
    @staticmethod
    def format_wishlist_response(wishlist_items):
        formatted_items = []
        for item in wishlist_items:
            formatted_items.append({
                "wishlist_id": item.id,
                "created_at": item.created_at,
                "game": item.user_games.serialize() if item.user_games else None
            })
        return formatted_items