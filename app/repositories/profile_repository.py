from app.models.profile import Profile
from app.extensions import db

class ProfileRepository:
    @staticmethod
    def create(user_id: int, first_name: str, last_name: str, country: str) -> Profile:
        profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name, country=country)
        db.session.add(profile)
        db.session.flush()
        return profile