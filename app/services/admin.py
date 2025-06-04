# Admin Service
from app.repositories.admin import AdminRepository
from typing import List, Optional, Dict, Any
import requests
import json
import logging

class AdminService:
    @staticmethod
    def get_all_games():
        return AdminRepository.get_all_games()
    
    @staticmethod
    def get_game_by_id(game_id: int):
        return AdminRepository.get_game_by_id(game_id)
    
    @staticmethod
    def create_game(game_data: Dict[str, Any]):
        required_fields = ['title', 'price', 'release_year', 'category', 'platform']
        for field in required_fields:
            if field not in game_data or not game_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        return AdminRepository.create_game(game_data)
    
    @staticmethod
    def update_game(game_id: int, game_data: Dict[str, Any]):
        return AdminRepository.update_game(game_id, game_data)
    
    @staticmethod
    def delete_game(game_id: int):
        return AdminRepository.delete_game(game_id)
    
    @staticmethod
    def fetch_game_data_from_steam(app_id: str):
        try:
            response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}")
            if response.status_code == 200:
                data = response.json()
                if data[app_id]["success"]:
                    return data[app_id]["data"]
            return None
        except Exception as e:
            logging.error(f"Error fetching game data from Steam: {str(e)}")
            return None
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        return AdminRepository.is_admin(user_id)
