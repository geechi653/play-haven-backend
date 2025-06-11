from typing import Optional, Dict, Any
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.extensions import db
from app.utils.validators import is_valid_email, is_valid_username
from werkzeug.security import generate_password_hash


class UserService:
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """Get user by ID"""
        return UserRepository.get_by_id(user_id)
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """Get user by username"""
        return UserRepository.get_by_username(username)
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        return UserRepository.get_by_email(email)
    
    @staticmethod
    def update_user(user_id: int, user_data: Dict[str, Any]) -> User:
        """Update user information"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User not found with id {user_id}")
        
        update_data = {}
        
        # Validate and update email
        if 'email' in user_data:
            new_email = user_data['email'].strip()
            if not new_email:
                raise ValueError("Email cannot be empty")
            if not is_valid_email(new_email):
                raise ValueError("Invalid email format")
            
            # Check if email is already taken by another user
            existing_user = UserRepository.get_by_email(new_email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already taken")
            
            update_data['email'] = new_email
        
        # Validate and update username
        if 'username' in user_data:
            new_username = user_data['username'].strip()
            if not new_username:
                raise ValueError("Username cannot be empty")
            if not is_valid_username(new_username):
                raise ValueError("Invalid username format")
            
            # Check if username is already taken by another user
            existing_user = UserRepository.get_by_username(new_username)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Username already taken")
            
            update_data['username'] = new_username
        
        # Update password if provided
        if 'password' in user_data:
            new_password = user_data['password']
            if not new_password:
                raise ValueError("Password cannot be empty")
            update_data['password'] = generate_password_hash(new_password)
        
        # Update is_active status if provided
        if 'is_active' in user_data:
            update_data['is_active'] = bool(user_data['is_active'])
        
        try:
            updated_user = UserRepository.update_user(user_id, **update_data)
            db.session.commit()
            return updated_user
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def deactivate_user(user_id: int) -> User:
        """Deactivate user account"""
        try:
            user = UserRepository.update_user(user_id, is_active=False)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def activate_user(user_id: int) -> User:
        """Activate user account"""
        try:
            user = UserRepository.update_user(user_id, is_active=True)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_user_with_profile(user_id: int) -> Optional[User]:
        """Get user with profile information"""
        return UserRepository.get_user_with_profile(user_id)
