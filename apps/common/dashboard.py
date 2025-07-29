"""
Функции для дашборда Django Unfold
"""
from django.db.models import Count
from django.contrib.auth.models import User
from apps.surveys.models import Survey


def dashboard_callback(request, context):
    """
    Функция для создания дашборда с метриками
    """
    # Получение статистики
    total_surveys = Survey.objects.count()
    active_surveys = Survey.objects.filter(is_active=True).count()
    inactive_surveys = total_surveys - active_surveys
    total_users = User.objects.count()
    
    # Последние опросы
    recent_surveys = Survey.objects.select_related('created_by').order_by('-created_at')[:5]
    
    context.update({
        'dashboard_stats': {
            'total_surveys': total_surveys,
            'active_surveys': active_surveys,
            'inactive_surveys': inactive_surveys,
            'total_users': total_users,
        },
        'recent_surveys': recent_surveys,
    })
    
    return context 