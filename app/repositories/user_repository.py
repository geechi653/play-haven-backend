from app.extensions import db
from app.models.user import User
from sqlalchemy import select
from typing import Optional

class UserRepository:
    @staticmethod
    def create_user(email: str) -> User:
        """Create new user"""
        user = User() 
        user.email = email
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        stmt = select(User).where(User.id == user_id)
        result = db.session.execute(stmt)
        user = result.scalars().first()
        return user
    
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get user by ID"""
        stmt = select(User).where(User.email == email)
        result = db.session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def get_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        stmt = select(User).where(User.username == username)
        result = db.session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def update(user: User) -> User:
        """Update the user"""
        db.session.commit()
        return user
    
    
    @staticmethod
    def delete(user: User) -> None:
        """Delete the user"""
        db.session.delete(user)
        db.session.commit()