"""
Функции для определения окружения в Django Unfold
"""
from django.conf import settings


def environment_callback(request):
    """
    Функция для отображения текущего окружения в Unfold
    """
    if settings.DEBUG:
        return ["Development", "warning"]
    
    return ["Production", "success"] 