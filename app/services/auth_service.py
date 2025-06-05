from typing import Optional
from app.repositories.user_repository import UserRepository
from app.models.user import User



class AuthService:
    pass
    @staticmethod
    def register(email: str, username: str, first_name: str, last_name: str, country: str, password: str) -> User:
        if UserRepository.get_by_email(email):
            raise ValueError("Email already taken")

        if UserRepository.get_by_username(username):
            raise ValueError("Username already taken")

        user = UserRepository.create_user(
            email, username, first_name, last_name, country, password)
       
        ProfileRepository.create(user.id) #todo error will be gone after adding Profile repository
        return user

