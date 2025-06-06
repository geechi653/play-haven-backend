from app.models.profile import Profile
from app.extensions import db
from typing import Optional

class ProfileRepository:

    @staticmethod
    def create_profile(user_id: int, first_name: str, last_name: str, country: str) -> Profile:
        profile = Profile(user_id=user_id, first_name=first_name, last_name=last_name, country=country)
        db.session.add(profile)
        db.session.flush()
        return profile
    

    @staticmethod
    def get_profile_by_user_id(user_id: int) -> Optional[Profile]:
        return db.session.query(Profile).filter_by(user_id=user_id).first()
    
    @staticmethod
    def get_profile_by_profile_id(profile_id: int) -> Optional[Profile]:
        return db.session.query(Profile).filter_by(profile_id=profile_id).first()
        

    @staticmethod
    def update_profile_by_user_id(user_id: int, **kwargs) -> bool:
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            raise ValueError(f"Profile for user_id {user_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        db.session.flush()
        return profile
    

    @staticmethod
    def update_profile_by_profile_id(profile_id: int, **kwargs) -> Profile:
        profile = db.session.get(Profile, profile_id)
        if not profile:
            raise ValueError(f"Profile with id {profile_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        db.session.flush()
        return profile
    

    @staticmethod
    def delete_profile_by_user_id(user_id: int) -> Profile:
        profile = db.session.query(Profile).filter_by(user_id=user_id).first()
        if not profile:
            return False
    
        db.session.delete(profile)
        db.session.flush()
        return True
    

    @staticmethod
    def delete_profile_by_profile_id(profile_id: int) -> Profile:
        profile = db.session.get(Profile, profile_id)
        if not profile:
            raise ValueError(f"Profile with id {profile_id} not found")
    
        db.session.delete(profile)
        db.session.flush()
        return profile
        
    