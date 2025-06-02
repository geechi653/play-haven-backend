# Admin Repository
from app.extensions import db
from app.models.user import User
from sqlalchemy import select
from typing import List, Optional

class AdminRepository:
    @staticmethod
    def get_all_games():
        from app.models.game import Game
        stmt = select(Game)
        games = db.session.execute(stmt).scalars().all()
        return games
    
    @staticmethod
    def get_game_by_id(game_id: int):
        from app.models.game import Game
        stmt = select(Game).where(Game.id == game_id)
        game = db.session.execute(stmt).scalar_one_or_none()
        return game
    
    @staticmethod
    def create_game(game_data: dict):
        from app.models.game import Game
        game = Game()
        
        game.title = game_data.get('title')
        game.price = game_data.get('price')
        game.release_year = game_data.get('release_year')
        game.category = game_data.get('category')
        game.platform = game_data.get('platform')
        
        if 'status' in game_data:
            game.status = game_data.get('status')
        if 'description' in game_data:
            game.description = game_data.get('description')
        if 'rating' in game_data:
            game.rating = game_data.get('rating')
        if 'image_url' in game_data:
            game.image_url = game_data.get('image_url')
        
        db.session.add(game)
        db.session.commit()
        return game
    
    @staticmethod
    def update_game(game_id: int, game_data: dict):
        game = AdminRepository.get_game_by_id(game_id)
        
        if not game:
            return None
        
        if 'title' in game_data:
            game.title = game_data.get('title')
        if 'price' in game_data:
            game.price = game_data.get('price')
        if 'release_year' in game_data:
            game.release_year = game_data.get('release_year')
        if 'status' in game_data:
            game.status = game_data.get('status')
        if 'category' in game_data:
            game.category = game_data.get('category')
        if 'description' in game_data:
            game.description = game_data.get('description')
        if 'platform' in game_data:
            game.platform = game_data.get('platform')
        if 'rating' in game_data:
            game.rating = game_data.get('rating')
        if 'image_url' in game_data:
            game.image_url = game_data.get('image_url')
        
        db.session.commit()
        return game
    
    @staticmethod
    def delete_game(game_id: int):
        game = AdminRepository.get_game_by_id(game_id)
        
        if not game:
            return False
        
        db.session.delete(game)
        db.session.commit()
        return True
    
    @staticmethod
    def get_admin_users() -> List[User]:
        stmt = select(User).where(User.is_admin == True)
        admin_users = db.session.execute(stmt).scalars().all()
        return admin_users
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        stmt = select(User).where(User.id == user_id, User.is_admin == True)
        admin_user = db.session.execute(stmt).scalar_one_or_none()
        return admin_user is not None
    
    @staticmethod
    def update_game(game_id: int, game_data: dict):
        """Update an existing game"""
        game = AdminRepository.get_game_by_id(game_id)
        
        if not game:
            return None
        
        if 'title' in game_data:
            game.title = game_data.get('title')
        if 'price' in game_data:
            game.price = game_data.get('price')
        if 'release_year' in game_data:
            game.release_year = game_data.get('release_year')
        if 'status' in game_data:
            game.status = game_data.get('status')
        if 'category' in game_data:
            game.category = game_data.get('category')
        if 'description' in game_data:
            game.description = game_data.get('description')
        if 'platform' in game_data:
            game.platform = game_data.get('platform')
        if 'rating' in game_data:
            game.rating = game_data.get('rating')
        if 'image_url' in game_data:
            game.image_url = game_data.get('image_url')
        
        db.session.commit()
        return game
    
    @staticmethod
    def delete_game(game_id: int):
        """Delete a game"""
        game = AdminRepository.get_game_by_id(game_id)
        
        if not game:
            return False
        
        db.session.delete(game)
        db.session.commit()
        return True
    
    @staticmethod
    def get_admin_users() -> List[User]:
        """Get all admin users"""
        stmt = select(User).where(User.is_admin == True)
        admin_users = db.session.execute(stmt).scalars().all()
        return admin_users
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Check if a user is an admin"""
        stmt = select(User).where(User.id == user_id, User.is_admin == True)
        admin_user = db.session.execute(stmt).scalar_one_or_none()
        return admin_user is not None
