from app.repositories.wishlist_item import WishlistItemRepository
from app.models.user import User
from app.extensions import db
from app.services.steam_service import SteamService
from sqlalchemy import select

class WishlistService:
    @staticmethod
    def get_user_wishlist(user_id: int):
        return WishlistItemRepository.get_user_wishlist(user_id)
    
    @staticmethod
    def get_wishlist_item(user_id: int, steam_game_id: int):
        return WishlistItemRepository.get_wishlist_item(user_id, steam_game_id)
    
    @staticmethod
    def add_to_wishlist(user_id: int, steam_game_id: int):
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
        
        return WishlistItemRepository.add_to_wishlist(user_id, steam_game_id)
    
    @staticmethod
    def delete_from_wishlist(user_id: int, steam_game_id: int):
        return WishlistItemRepository.delete_from_wishlist(user_id, steam_game_id)
    
    @staticmethod
    def format_wishlist_response(wishlist_items):
        steam_service = SteamService()
        formatted_items = []
        for item in wishlist_items:
            # Get game details from Steam API
            game_details = steam_service.get_game_details(item.steam_game_id)
            formatted_items.append({
                "wishlist_id": item.id,
                "created_at": item.created_at,
                "game": game_details  # Steam game details
            })
        return formatted_items