from django import forms
from django.core.validators import RegexValidator


class NIIEDULoginForm(forms.Form):
    """Форма для аутентификации через NII EDU"""
    
    login = forms.CharField(
        label='Логин',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': '462221101004',
            'autocomplete': 'username'
        }),
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Логин должен содержать только цифры'
            )
        ],
        help_text='Введите ваш логин (только цифры)'
    )
    
    password = forms.CharField(
        label='Пароль',
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Введите пароль',
            'autocomplete': 'current-password'
        }),
        help_text='Введите ваш пароль от NII EDU'
    )
    
    def clean_login(self):
        """Очистка и валидация логина"""
        login = self.cleaned_data['login']
        # Убираем пробелы
        login = login.strip()
        
        if not login:
            raise forms.ValidationError('Логин не может быть пустым')
        
        return login
    
    def clean_password(self):
        """Очистка и валидация пароля"""
        password = self.cleaned_data['password']
        
        if not password:
            raise forms.ValidationError('Пароль не может быть пустым')
        
        if len(password) < 4:
            raise forms.ValidationError('Пароль должен содержать минимум 4 символа')
        
        return password 