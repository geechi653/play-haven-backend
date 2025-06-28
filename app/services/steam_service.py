import requests
import logging
import time
from flask import current_app
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class SteamService:
    # In-memory cache for game details
    _game_cache = {}
    _cache_expiry = 3600  # Cache expiry in seconds (1 hour)
    _last_fetch_time = {}  # Throttling tracker

    def __init__(self):
        self.api_key = current_app.config['STEAM_API_KEY']
        self.base_url = "https://api.steampowered.com"
        self.store_url = "https://store.steampowered.com/api"

    def _sanitize_html_description(self, description):
        """Clean HTML description from Steam API"""
        if not description:
            return ""
            
        # Replace problematic HTML tags with proper formatting
        # Replace <br> tags with newlines
        cleaned = re.sub(r'<br\s*/?>', '\n', description)
        
        # Handle lists
        cleaned = re.sub(r'<ul[^>]*>', '\n', cleaned)
        cleaned = re.sub(r'</ul>', '\n', cleaned)
        cleaned = re.sub(r'<li[^>]*>', '• ', cleaned)
        cleaned = re.sub(r'</li>', '\n', cleaned)
        
        # Remove other common HTML tags
        cleaned = re.sub(r'<h[1-6][^>]*>(.*?)</h[1-6]>', r'\1\n', cleaned)
        cleaned = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n', cleaned)
        cleaned = re.sub(r'<div[^>]*>(.*?)</div>', r'\1', cleaned)
        cleaned = re.sub(r'<span[^>]*>(.*?)</span>', r'\1', cleaned)
        
        cleaned = re.sub(r'<[^>]+>', '', cleaned)
        
        cleaned = cleaned.replace('&nbsp;', ' ')
        cleaned = cleaned.replace('&amp;', '&')
        cleaned = cleaned.replace('&lt;', '<')
        cleaned = cleaned.replace('&gt;', '>')
        cleaned = cleaned.replace('&quot;', '"')
        cleaned = cleaned.replace('&#39;', "'")
        
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        
        return cleaned.strip()

    def _format_game_data(self, game_data):
        """Convert Steam API game data to our format"""
        try:
            price = float(game_data.get('price_overview', {}).get('final', 0)) / 100 if game_data.get('price_overview') else 0.00
            
            release_date = game_data.get('release_date', {})
            release_year = None
            if release_date and release_date.get('date'):
                try:
                    date_str = release_date.get('date')
                    for fmt in ['%d %b, %Y', '%b %d, %Y', '%B %d, %Y', '%Y']:
                        try:
                            release_year = datetime.strptime(date_str, fmt).year
                            break
                        except ValueError:
                            continue
                except Exception as e:
                    logger.error(f"Error parsing date {release_date.get('date')}: {e}")
            
            categories = ', '.join([category.get('description') for category in game_data.get('categories', [])]) if game_data.get('categories') else None
            
            platforms = []
            if game_data.get('platforms'):
                if game_data['platforms'].get('windows'):
                    platforms.append('Windows')
                if game_data['platforms'].get('mac'):
                    platforms.append('Mac')
                if game_data['platforms'].get('linux'):
                    platforms.append('Linux')
            
            description = game_data.get('detailed_description') or game_data.get('short_description') or ""
            sanitized_description = self._sanitize_html_description(description)
            
            formatted_game = {
                "id": game_data.get('steam_appid'),
                "title": game_data.get('name'),
                "price": str(price),
                "release_year": release_year or datetime.now().year,
                "status": "Available" if game_data.get('is_free') == False else "Free",
                "category": categories or "Uncategorized",
                "description": sanitized_description,
                "platform": ", ".join(platforms) or "PC",
                "rating": game_data.get('metacritic', {}).get('score', 0) / 10 if game_data.get('metacritic') else None,
                "image_url": game_data.get('header_image')
            }
            return formatted_game
        except Exception as e:
            logger.error(f"Error formatting game data: {e}")
            return None

    def get_top_games(self, limit=30, offset=0):
        """Get top most played games"""
        try:
            cache_key = f"top_games_{limit}_{offset}"
            current_time = time.time()
            
            if cache_key in self._game_cache:
                cache_entry = self._game_cache[cache_key]
                if current_time - cache_entry['timestamp'] < self._cache_expiry:
                    logger.info(f"Cache hit for top_games")
                    return cache_entry['data']
            
            if 'last_request' in self._last_fetch_time:
                elapsed = current_time - self._last_fetch_time['last_request']
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)
            
            self._last_fetch_time['last_request'] = time.time()
            
            url = f"{self.base_url}/ISteamChartsService/GetMostPlayedGames/v1/"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            top_games = []
            ranks = data.get('response', {}).get('ranks', [])
            # Support offset and limit for paging
            for i, rank in enumerate(ranks[offset:offset+limit]):
                app_id = rank.get('appid')
                if app_id:
                    game_details = self.get_game_details(app_id)
                    if game_details:
                        top_games.append(game_details)
                if len(top_games) >= limit:
                    break
            self._game_cache[cache_key] = {
                'data': top_games,
                'timestamp': time.time()
            }
            return top_games
        except Exception as e:
            logger.error(f"Error fetching top games: {e}")
            return []

    def get_discounted_games(self, limit=10):
        """Get discounted games"""
        try:
            cache_key = f"discounted_games_{limit}"
            current_time = time.time()
            
            if cache_key in self._game_cache:
                cache_entry = self._game_cache[cache_key]
                if current_time - cache_entry['timestamp'] < self._cache_expiry:
                    logger.info(f"Cache hit for discounted_games")
                    return cache_entry['data']
            
            if 'last_request' in self._last_fetch_time:
                elapsed = current_time - self._last_fetch_time['last_request']
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)
            
            self._last_fetch_time['last_request'] = time.time()
            
            url = f"{self.store_url}/featuredcategories/?l=english"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            specials = data.get('specials', {}).get('items', [])
            
            discounted_games = []
            for i, game in enumerate(specials[:limit]):
                app_id = game.get('id')
                if app_id:
                    game_details = self.get_game_details(app_id)
                    if game_details:
                        discounted_games.append(game_details)
                        
                if len(discounted_games) >= limit:
                    break
            
            self._game_cache[cache_key] = {
                'data': discounted_games,
                'timestamp': time.time()
            }
                    
            return discounted_games
        except Exception as e:
            logger.error(f"Error fetching discounted games: {e}")
            return []

    def get_featured_games(self, limit=10):
        """Get featured games"""
        try:
            cache_key = f"featured_games_{limit}"
            current_time = time.time()
            
            if cache_key in self._game_cache:
                cache_entry = self._game_cache[cache_key]
                if current_time - cache_entry['timestamp'] < self._cache_expiry:
                    logger.info(f"Cache hit for featured_games")
                    return cache_entry['data']
            
            if 'last_request' in self._last_fetch_time:
                elapsed = current_time - self._last_fetch_time['last_request']
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)
            
            self._last_fetch_time['last_request'] = time.time()
            
            url = f"{self.store_url}/featured/?l=english"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            featured_games = data.get('featured_win', [])
            
            formatted_games = []
            for i, game in enumerate(featured_games[:limit]):
                app_id = game.get('id')
                if app_id:
                    game_details = self.get_game_details(app_id)
                    if game_details:
                        formatted_games.append(game_details)
                        
                if len(formatted_games) >= limit:
                    break
            
            # Store in cache
            self._game_cache[cache_key] = {
                'data': formatted_games,
                'timestamp': time.time()
            }
                    
            return formatted_games
        except Exception as e:
            logger.error(f"Error fetching featured games: {e}")
            return []

    def get_game_details(self, app_id):
        """Get detailed information for a specific game"""
        try:
            cache_key = str(app_id)
            current_time = time.time()
            
            if cache_key in self._game_cache:
                cache_entry = self._game_cache[cache_key]
                if current_time - cache_entry['timestamp'] < self._cache_expiry:
                    logger.info(f"Cache hit for app_id: {app_id}")
                    return cache_entry['data']
            
            if 'last_request' in self._last_fetch_time:
                elapsed = current_time - self._last_fetch_time['last_request']
                if elapsed < 0.5:  # 500ms
                    time.sleep(0.5 - elapsed)
            
            self._last_fetch_time['last_request'] = time.time()
            
            # Always add l=english to the appdetails URL
            url = f"{self.store_url}/appdetails?appids={app_id}&l=english"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and data.get(str(app_id), {}).get('success'):
                game_data = data.get(str(app_id), {}).get('data', {})
                formatted_data = self._format_game_data(game_data)
                
                if formatted_data:
                    self._game_cache[cache_key] = {
                        'data': formatted_data,
                        'timestamp': time.time()
                    }
                
                return formatted_data
            return None
        except Exception as e:
            logger.error(f"Error fetching game details for app_id {app_id}: {e}")
            return None

    def search_games(self, query, limit=20):
        """Search for games by name"""
        try:
            cache_key = f"search_{query}_{limit}"
            current_time = time.time()
            
            if cache_key in self._game_cache:
                cache_entry = self._game_cache[cache_key]
                if current_time - cache_entry['timestamp'] < self._cache_expiry:
                    logger.info(f"Cache hit for search_games: {query}")
                    return cache_entry['data']
            
            if 'last_request' in self._last_fetch_time:
                elapsed = current_time - self._last_fetch_time['last_request']
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)
            
            self._last_fetch_time['last_request'] = time.time()
            
            url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            search_results = []
            if data and 'items' in data:
                # Get the first 'limit' results
                for i, item in enumerate(data['items'][:limit]):
                    app_id = item.get('id')
                    if app_id:
                        # Get detailed info for each game
                        game_details = self.get_game_details(app_id)
                        if game_details:
                            search_results.append(game_details)
                    
                    if len(search_results) >= limit:
                        break
            
            # Store in cache
            self._game_cache[cache_key] = {
                'data': search_results,
                'timestamp': time.time()
            }
                
            return search_results
        except Exception as e:
            logger.error(f"Error searching games with query '{query}': {e}")
            return []

    def get_game_news(self, app_id, count=5, maxlength=500):
        """Fetch news for a specific game from Steam API"""
        try:
            cache_key = f"news_{app_id}_{count}_{maxlength}"
            current_time = time.time()
            if cache_key in self._game_cache:
                cache_entry = self._game_cache[cache_key]
                if current_time - cache_entry['timestamp'] < self._cache_expiry:
                    logger.info(f"Cache hit for news: {app_id}")
                    return cache_entry['data']

            if 'last_request' in self._last_fetch_time:
                elapsed = current_time - self._last_fetch_time['last_request']
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)
            self._last_fetch_time['last_request'] = time.time()

            url = f"{self.base_url}/ISteamNews/GetNewsForApp/v0002/"
            params = {
                "appid": app_id,
                "count": count,
                "maxlength": maxlength,
                "format": "json"
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            news_items = data.get("appnews", {}).get("newsitems", [])

            formatted_news = [
                {
                    "title": item.get("title"),
                    "date": datetime.utcfromtimestamp(item.get("date")).strftime("%Y-%m-%d"),
                    "summary": item.get("contents"),
                    "url": item.get("url")
                }
                for item in news_items
            ]

            self._game_cache[cache_key] = {
                "data": formatted_news,
                "timestamp": time.time()
            }
            return formatted_news
        except Exception as e:
            logger.error(f"Error fetching news for app_id {app_id}: {e}")
            return []
