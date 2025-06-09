from app.extensions import db
from app.models.wishlist_item import WishlistItem
from sqlalchemy import select
from typing import List, Optional

class WishlistItemRepository:
    @staticmethod
    def get_user_wishlist(user_id: int) -> List[WishlistItem]:
        stmt = select(WishlistItem).where(WishlistItem.user_id == user_id)
        wishlist_items = db.session.execute(stmt).scalars().all()
        return wishlist_items
    
    @staticmethod
    def get_wishlist_item(user_id: int, game_id: int) -> Optional[WishlistItem]:
        stmt = select(WishlistItem).where(
            WishlistItem.user_id == user_id,
            WishlistItem.game_id == game_id
        )
        wishlist_item = db.session.execute(stmt).scalar_one_or_none()
        return wishlist_item
    
    @staticmethod
    def add_to_wishlist(user_id: int, game_id: int) -> WishlistItem:
        existing_wishlist_item = WishlistItemRepository.get_wishlist_item(user_id, game_id)
        if existing_wishlist_item:
            return existing_wishlist_item
        
        wishlist_item = WishlistItem()
        wishlist_item.user_id = user_id
        wishlist_item.game_id = game_id
        
        db.session.add(wishlist_item)
        db.session.commit()
        return wishlist_item
    
    @staticmethod
    def delete_from_wishlist(user_id: int, game_id: int) -> bool:
        wishliset_item = WishlistItemRepository.get_wishlist_item(user_id, game_id)
        
        if not wishliset_item:  
            return False
        
        db.session.delete(wishliset_item)
        db.session.commit()
        return True