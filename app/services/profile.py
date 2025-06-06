from typing import Optional, Dict, Any
from app.repositories.profile_repository import ProfileRepository
from app.models.profile import Profile
from app.extensions import db


class ProfileService:
    
    @staticmethod
    def create_user_profile(user_id: int, profile_data: Dict[str, Any]) -> Profile:
        existing_profile = ProfileRepository.get_profile_by_user_id(user_id)
        if existing_profile:
            raise ValueError(f"Profile already exists for user_id {user_id}")
        
        required_fields = ['first_name', 'last_name', 'country']
        for field in required_fields:
            if not profile_data.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        first_name = profile_data['first_name'].strip().title()
        last_name = profile_data['last_name'].strip().title()
        country = profile_data['country'].strip().upper()
        
        try:
            profile = ProfileRepository.create_profile(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                country=country
            )

            additional_fields = {
                'avatar_url': profile_data.get('avatar_url'),
                'address': profile_data.get('address'),
                'city': profile_data.get('city'),
                'state': profile_data.get('state'),
                'zip_code': profile_data.get('zip_code')
            }
            
            update_data = {k: v for k, v in additional_fields.items() if v is not None}
            if update_data:
                ProfileRepository.update_profile_by_profile_id(profile.id, **update_data)
            db.session.commit()
            return profile
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_user_profile(user_id: int) -> Optional[Profile]:
        return ProfileRepository.get_profile_by_user_id(user_id)
    
    @staticmethod
    def get_profile_by_profile_id(profile_id: int) -> Optional[Profile]:
        return ProfileRepository.get_profile_by_profile_id(profile_id)
    
    @staticmethod
    def update_user_profile(user_id: int, profile_data: Dict[str, Any]) -> Profile:
        profile = ProfileRepository.get_profile_by_user_id(user_id)
        if not profile:
            raise ValueError(f"Profile not found for user_id {user_id}")
        
        update_data = {}
        
        if 'first_name' in profile_data:
            if not profile_data['first_name'].strip():
                raise ValueError("First name cannot be empty")
            update_data['first_name'] = profile_data['first_name'].strip().title()
        
        if 'last_name' in profile_data:
            if not profile_data['last_name'].strip():
                raise ValueError("Last name cannot be empty")
            update_data['last_name'] = profile_data['last_name'].strip().title()
        
        if 'country' in profile_data:
            if not profile_data['country'].strip():
                raise ValueError("Country cannot be empty")
            update_data['country'] = profile_data['country'].strip().upper()
        
        optional_fields = ['avatar_url', 'address', 'city', 'state', 'zip_code']
        for field in optional_fields:
            if field in profile_data:
                update_data[field] = profile_data[field]
        
        try:
            updated_profile = ProfileRepository.update_profile_by_user_id(user_id, **update_data)
            db.session.commit()
            return updated_profile
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_user_profile(user_id: int) -> bool:
        try:
            profile = ProfileRepository.get_profile_by_user_id(user_id)
            if not profile:
                return False
            ProfileRepository.delete_profile_by_user_id(user_id)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_avatar(user_id: int, avatar_url: str) -> Profile:
        if not avatar_url:
            raise ValueError("Avatar URL cannot be empty")
        try:
            profile = ProfileRepository.update_profile_by_user_id(
                user_id, 
                avatar_url=avatar_url
            )
            db.session.commit()
            return profile
        except Exception as e:
            db.session.rollback()
            raise e