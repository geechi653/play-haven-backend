from typing import Optional
from app.repositories.example import UserRepository
from app.models.user import User



class AuthService:
    @staticmethod
    def register(email: str, username: str, first_name: str, last_name: str, country: str, password: str) -> User:
        if UserRepository.get_by_email(email):
            raise ValueError("Email already taken")
        return UserRepository.create_user(email=email)

        if UserRepository.get_by_username(username):
            raise ValueError("Username already taken")
        return UserRepository.create_user(username=username)

        user = UserRepository.create_user(
            email, username, first_name, last_name, country, password)

    @staticmethod
    def get_user_by_id(id: int) -> Optional[User]:
        return UserRepository.get_by_id(id)
