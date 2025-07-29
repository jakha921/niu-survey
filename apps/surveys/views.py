from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Survey
from .forms import NIIEDULoginForm
from .services import NIIEDUAuthService


# ========== WEB VIEWS ==========

class SurveyListView(ListView):
    """Список всех активных опросов"""
    model = Survey
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'
    paginate_by = 12
    
    def get_queryset(self):
        return Survey.objects.filter(is_active=True).select_related('created_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Доступные опросы'
        return context


class SurveyDetailView(DetailView):
    """Детальная страница опроса с встроенной Google Form"""
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Survey.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['embed_url'] = self.object.get_google_form_embed_url()
        
        # Проверяем, требуется ли аутентификация
        if self.object.is_login_req:
            context['requires_auth'] = True
            context['login_form'] = NIIEDULoginForm()
            
            # Проверяем кэшированную аутентификацию
            session_login = self.request.session.get('niiedu_login')
            if session_login:
                cached_auth = NIIEDUAuthService.check_cached_auth(session_login)
                if cached_auth:
                    context['is_authenticated'] = True
                    context['user_data'] = cached_auth
                else:
                    # Очищаем сессию если кэш истек
                    self.request.session.pop('niiedu_login', None)
        
        return context


# ========== ДОПОЛНИТЕЛЬНЫЕ VIEWS ==========

def survey_embed_view(request, slug):
    """
    Страница только с встроенной Google Form (для iframe)
    """
    survey = get_object_or_404(Survey, slug=slug, is_active=True)
    
    return render(request, 'surveys/survey_embed.html', {
        'survey': survey,
        'embed_url': survey.get_google_form_embed_url(),
    })


@csrf_exempt
def niiedu_login_view(request, slug):
    """
    Обработка аутентификации через NII EDU API
    """
    survey = get_object_or_404(Survey, slug=slug, is_active=True)
    
    if not survey.is_login_req:
        return redirect('surveys:survey_detail', slug=slug)
    
    if request.method == 'POST':
        form = NIIEDULoginForm(request.POST)
        
        if form.is_valid():
            login = form.cleaned_data['login']
            password = form.cleaned_data['password']
            
            # Выполняем аутентификацию
            auth_result = NIIEDUAuthService.login(login, password)
            
            if auth_result['success']:
                # Сохраняем логин в сессии
                request.session['niiedu_login'] = login
                messages.success(request, 'Аутентификация успешна!')
                return redirect('surveys:survey_detail', slug=slug)
            else:
                messages.error(request, f'Ошибка аутентификации: {auth_result["error"]}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    
    else:
        form = NIIEDULoginForm()
    
    return render(request, 'surveys/survey_detail.html', {
        'survey': survey,
        'title': survey.title,
        'embed_url': survey.get_google_form_embed_url(),
        'requires_auth': True,
        'login_form': form,
        'is_authenticated': False
    })


def niiedu_logout_view(request, slug):
    """
    Выход из системы NII EDU
    """
    survey = get_object_or_404(Survey, slug=slug, is_active=True)
    
    # Очищаем кэш аутентификации
    session_login = request.session.get('niiedu_login')
    if session_login:
        NIIEDUAuthService.logout(session_login)
        request.session.pop('niiedu_login', None)
    
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('surveys:survey_detail', slug=slug) 