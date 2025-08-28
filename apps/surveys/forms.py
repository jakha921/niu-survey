from django import forms
from django.core.validators import RegexValidator


class NIIEDULoginForm(forms.Form):
    """Форма для аутентификации через NII EDU"""
    
    login = forms.CharField(
        label='Login',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': '462221101004',
            'autocomplete': 'username'
        }),
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='Login faqat raqamlardan iborat bo\'lishi kerak'
            )
        ],
        help_text='Login kiriting (faqat raqamlar)'
    )
    
    password = forms.CharField(
        label='Parol',
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent',
            'placeholder': 'Parol kiriting',
            'autocomplete': 'current-password'
        }),
        help_text='NII EDU parolingizni kiriting'
    )
    
    def clean_login(self):
        """Очистка и валидация логина"""
        login = self.cleaned_data['login']
        # Убираем пробелы
        login = login.strip()
        
        if not login:
            raise forms.ValidationError('Login bo\'sh bo\'lishi mumkin emas')
        
        return login
    
    def clean_password(self):
        """Очистка и валидация пароля"""
        password = self.cleaned_data['password']
        
        if not password:
            raise forms.ValidationError('Parol bo\'sh bo\'lishi mumkin emas')
        
        if len(password) < 4:
            raise forms.ValidationError('Parol kamida 4 belgidan iborat bo\'lishi kerak')
        
        return password 