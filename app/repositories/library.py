# Library Repository
from app.extensions import db
from app.models.user_library import UserLibrary
from sqlalchemy import select
from typing import List, Optional

class LibraryRepository:
    @staticmethod
    def get_user_library(user_id: int) -> List[UserLibrary]:
        stmt = select(UserLibrary).where(UserLibrary.user_id == user_id)
        library_items = db.session.execute(stmt).scalars().all()
        return library_items
    
    @staticmethod
    def get_library_item(user_id: int, steam_game_id: int) -> Optional[UserLibrary]:
        stmt = select(UserLibrary).where(
            UserLibrary.user_id == user_id,
            UserLibrary.steam_game_id == steam_game_id
        )
        library_item = db.session.execute(stmt).scalar_one_or_none()
        return library_item
    
    @staticmethod
    def add_to_library(user_id: int, steam_game_id: int) -> UserLibrary:
        existing_item = LibraryRepository.get_library_item(user_id, steam_game_id)
        if existing_item:
            return existing_item
        
        library_item = UserLibrary()
        library_item.user_id = user_id
        library_item.steam_game_id = steam_game_id
        
        db.session.add(library_item)
        db.session.commit()
        return library_item
    
    @staticmethod
    def remove_from_library(user_id: int, steam_game_id: int) -> bool:
        library_item = LibraryRepository.get_library_item(user_id, steam_game_id)
        
        if not library_item:
            return False
        
        db.session.delete(library_item)
        db.session.commit()
        return True
