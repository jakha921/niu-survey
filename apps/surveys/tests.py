from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Survey


class SurveyModelTests(TestCase):
    """Тесты модели Survey"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_survey_creation(self):
        """Тест создания опроса"""
        survey = Survey.objects.create(
            title='Тестовый опрос',
            google_form_url='https://docs.google.com/forms/d/test/viewform',
            description='Описание тестового опроса',
            created_by=self.user
        )
        
        self.assertEqual(survey.title, 'Тестовый опрос')
        self.assertTrue(survey.is_active)
        self.assertEqual(str(survey), 'Тестовый опрос')
    
    def test_survey_embed_url(self):
        """Тест генерации URL для встраивания"""
        survey = Survey.objects.create(
            title='Тестовый опрос',
            google_form_url='https://docs.google.com/forms/d/test/viewform',
            created_by=self.user
        )
        
        embed_url = survey.get_google_form_embed_url()
        self.assertIn('embedded=true', embed_url)
    
    def test_short_description(self):
        """Тест короткого описания"""
        long_description = 'Это очень длинное описание опроса' * 10
        survey = Survey.objects.create(
            title='Тестовый опрос',
            google_form_url='https://docs.google.com/forms/d/test/viewform',
            description=long_description,
            created_by=self.user
        )
        
        short_desc = survey.short_description
        self.assertTrue(len(short_desc) <= 53)  # 50 + '...'


class SurveyViewTests(TestCase):
    """Тесты представлений"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.survey = Survey.objects.create(
            title='Тестовый опрос',
            slug='testovyj-opros',
            google_form_url='https://docs.google.com/forms/d/test/viewform',
            description='Описание тестового опроса',
            created_by=self.user,
            is_active=True
        )
        
        self.inactive_survey = Survey.objects.create(
            title='Неактивный опрос', 
            slug='neaktivnyj-opros',
            google_form_url='https://docs.google.com/forms/d/test2/viewform',
            created_by=self.user,
            is_active=False
        )
    
    def test_survey_list_view(self):
        """Тест списка опросов"""
        response = self.client.get(reverse('surveys:survey_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый опрос')
        self.assertNotContains(response, 'Неактивный опрос')
    
    def test_survey_detail_view(self):
        """Тест детальной страницы опроса"""
        response = self.client.get(
            reverse('surveys:survey_detail', kwargs={'slug': self.survey.slug})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый опрос')
        self.assertContains(response, 'embedded=true')
    
    def test_survey_detail_inactive(self):
        """Тест доступа к неактивному опросу"""
        response = self.client.get(
            reverse('surveys:survey_detail', kwargs={'slug': self.inactive_survey.slug})
        )
        
        self.assertEqual(response.status_code, 404)
    
    def test_survey_embed_view(self):
        """Тест встроенной страницы опроса"""
        response = self.client.get(
            reverse('surveys:survey_embed', kwargs={'slug': self.survey.slug})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовый опрос')
    
    def test_survey_with_login_required(self):
        """Тест опроса с требованием авторизации"""
        # Создаем опрос с требованием авторизации
        auth_survey = Survey.objects.create(
            title='Опрос с авторизацией',
            slug='opros-s-avtorizaciej',
            google_form_url='https://docs.google.com/forms/d/test3/viewform',
            created_by=self.user,
            is_active=True,
            is_login_req=True
        )
        
        # Проверяем, что форма авторизации отображается
        response = self.client.get(
            reverse('surveys:survey_detail', kwargs={'slug': auth_survey.slug})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Autentifikatsiya Talab Qilinadi')
        self.assertContains(response, 'Tizimga Kirish')


 