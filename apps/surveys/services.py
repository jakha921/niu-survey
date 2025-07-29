import requests
import json
from django.conf import settings
from django.core.cache import cache
from typing import Optional, Dict, Any


class NIIEDUAuthService:
    """Сервис для аутентификации через NII EDU API"""
    
    BASE_URL = "https://student.niiedu.uz/rest/v1"
    LOGIN_URL = f"{BASE_URL}/auth/login"
    CACHE_TIMEOUT = 3600  # 1 час
    
    @classmethod
    def login(cls, login: str, password: str) -> Dict[str, Any]:
        """
        Аутентификация пользователя через NII EDU API
        
        Args:
            login: Логин пользователя (например, 462221101004)
            password: Пароль пользователя
            
        Returns:
            Dict с результатом аутентификации
        """
        try:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            data = {
                'login': login,
                'password': password
            }
            
            response = requests.post(
                cls.LOGIN_URL,
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                # Кэшируем успешную аутентификацию
                cache_key = f"niiedu_auth_{login}"
                cache.set(cache_key, result, cls.CACHE_TIMEOUT)
                
                return {
                    'success': True,
                    'data': result,
                    'message': 'Аутентификация успешна'
                }
            else:
                return {
                    'success': False,
                    'error': f'Ошибка аутентификации: {response.status_code}',
                    'details': response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Ошибка сети: {str(e)}'
            }
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Ошибка парсинга ответа: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Неожиданная ошибка: {str(e)}'
            }
    
    @classmethod
    def check_cached_auth(cls, login: str) -> Optional[Dict[str, Any]]:
        """
        Проверяет кэшированную аутентификацию
        
        Args:
            login: Логин пользователя
            
        Returns:
            Кэшированные данные аутентификации или None
        """
        cache_key = f"niiedu_auth_{login}"
        return cache.get(cache_key)
    
    @classmethod
    def logout(cls, login: str) -> bool:
        """
        Удаляет кэшированную аутентификацию
        
        Args:
            login: Логин пользователя
            
        Returns:
            True если кэш успешно очищен
        """
        cache_key = f"niiedu_auth_{login}"
        cache.delete(cache_key)
        return True 