from app.extensions import db
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository
from app.models.user import User


class AuthService:

    @staticmethod
    def register(email: str, username: str, first_name: str, last_name: str, country: str, password: str) -> User:
        if UserRepository.get_by_email(email):
            raise ValueError("Email already taken")

        if UserRepository.get_by_username(username):
            raise ValueError("Username already taken")

        try:
            user = UserRepository.create_user(email, username, password)
            db.session.flush()
            profile = ProfileRepository.create_profile(
                user_id=user.id, first_name=first_name, last_name=last_name, country=country)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Registration failed: {str(e)}")
