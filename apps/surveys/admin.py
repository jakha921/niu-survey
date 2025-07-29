from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RelatedDropdownFilter,
    ChoicesDropdownFilter,
)
from unfold.decorators import display
from simple_history.admin import SimpleHistoryAdmin

from .models import Survey


@admin.register(Survey)
class SurveyAdmin(ModelAdmin, SimpleHistoryAdmin):
    """
    Админ-панель для управления опросами с интеграцией Unfold
    """
    
    # Основные настройки списка
    list_display = [
        'title', 
        'is_active_display', 
        'google_form_link', 
        'short_description',
        'created_by',
        'created_at_display',
        'actions_display'
    ]
    
    list_filter = [
        'is_active',
        ('created_at', RangeDateFilter),
        ('created_by', RelatedDropdownFilter),
    ]
    
    search_fields = ['title', 'description']
    
    # Настройки readonly
    readonly_fields = ['created_at', 'updated_at', 'created_by', 'updated_by']
    
    # Группировка полей в форме
    fieldsets = [
        ('Основная информация', {
            'fields': ['title', 'description'],
            'classes': ['tab'],
        }),
        ('Интеграция с Google Forms', {
            'fields': ['google_form_url'],
            'classes': ['tab'],
            'description': 'Вставьте ссылку на ваш Google Form'
        }),
        ('Настройки', {
            'fields': ['is_active', 'is_login_req'],
            'classes': ['tab'],
        }),
        ('Служебная информация', {
            'fields': ['created_at', 'updated_at', 'created_by', 'updated_by'],
            'classes': ['collapse', 'tab'],
        }),
    ]
    
    # Настройки пагинации
    list_per_page = 25
    
    # Действия
    actions = ['make_active', 'make_inactive']
    
    @display(description='Статус', label=True)
    def is_active_display(self, obj):
        """Красивое отображение статуса активности"""
        if obj.is_active:
            return format_html(
                '<span class="badge badge-success">Активен</span>'
            )
        return format_html(
            '<span class="badge badge-danger">Неактивен</span>'
        )
    
    @display(description='Google Form', label=False)
    def google_form_link(self, obj):
        """Ссылка на Google Form с иконкой"""
        return format_html(
            '<a href="{}" target="_blank" class="button" style="color: #1976d2;">'
            '<i class="material-icons" style="vertical-align: middle; margin-right: 4px;">open_in_new</i>'
            'Открыть форму'
            '</a>',
            obj.google_form_url
        )
    
    @display(description='Дата создания', ordering='created_at')
    def created_at_display(self, obj):
        """Форматированная дата создания"""
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    
    @display(description='Действия', label=False)
    def actions_display(self, obj):
        """Быстрые действия для объекта"""
        edit_url = reverse('admin:surveys_survey_change', args=[obj.pk])
        delete_url = reverse('admin:surveys_survey_delete', args=[obj.pk])
        
        return format_html(
            '<a href="{}" class="button" style="margin-right: 5px;">'
            '<i class="material-icons">edit</i></a>'
            '<a href="{}" class="button button--danger">'
            '<i class="material-icons">delete</i></a>',
            edit_url, delete_url
        )
    
    def make_active(self, request, queryset):
        """Активировать выбранные опросы"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request, 
            f'{updated} опросов было активировано.'
        )
    make_active.short_description = 'Активировать выбранные опросы'
    
    def make_inactive(self, request, queryset):
        """Деактивировать выбранные опросы"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request, 
            f'{updated} опросов было деактивировано.'
        )
    make_inactive.short_description = 'Деактивировать выбранные опросы'
    
    def save_model(self, request, obj, form, change):
        """Автоматическое заполнение полей при сохранении"""
        if not change:  # Новый объект
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related(
            'created_by', 
            'updated_by'
        )
        
    # Настройки Unfold
    warn_unsaved_form = True
    
    # Дополнительные настройки для вкладок
    tab_overview = (
        ('Основная информация', {'fields': ['title', 'description']}),
    )
    
    tab_google_forms = (
        ('Google Forms', {'fields': ['google_form_url']}),
    )
    
    tab_settings = (
        ('Настройки', {'fields': ['is_active', 'is_login_req']}),
    ) 