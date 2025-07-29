from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import URLValidator
from django.utils.text import slugify
from simple_history.models import HistoricalRecords


class Survey(models.Model):
    """
    Модель опроса с интеграцией Google Forms
    """
    title = models.CharField(
        max_length=200,
        verbose_name='Название опроса',
        help_text='Название вашего опроса'
    )
    
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        default='',
        verbose_name='Slug (URL)',
        help_text='Автоматически генерируется из названия'
    )
    
    google_form_url = models.URLField(
        max_length=500,
        verbose_name='Ссылка на Google Form',
        help_text='Полная ссылка на Google Form для этого опроса',
        validators=[URLValidator(message='Введите корректную ссылку на Google Form')]
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Краткое описание опроса'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен',
        help_text='Показывать ли опрос пользователям'
    )
    
    is_login_req = models.BooleanField(
        default=False,
        verbose_name='Требуется авторизация',
        help_text='Требуется ли авторизация через NII EDU для доступа к опросу'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_surveys',
        verbose_name='Создал'
    )
    
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_surveys',
        verbose_name='Обновил'
    )
    
    # Отслеживание истории изменений
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['-created_at']
        db_table = 'surveys_survey'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """Ссылка на детальную страницу опроса"""
        return reverse('surveys:survey_detail', kwargs={'slug': self.slug})
    
    def get_google_form_embed_url(self):
        """
        Преобразует обычную ссылку Google Form в ссылку для встраивания
        """
        if 'viewform' in self.google_form_url:
            return self.google_form_url.replace('viewform', 'viewform?embedded=true')
        return self.google_form_url
    
    @property
    def short_description(self):
        """Короткое описание для админки"""
        if self.description:
            return self.description[:50] + '...' if len(self.description) > 50 else self.description
        return 'Описание не добавлено'
    
    def save(self, *args, **kwargs):
        """Переопределяем save для дополнительной логики"""
        # Автогенерация slug из title (даже если slug пустой)
        if not self.slug or self.slug == '':
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # Проверяем уникальность slug
            while Survey.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        # Здесь можно добавить логику валидации Google Forms URL
        super().save(*args, **kwargs) 