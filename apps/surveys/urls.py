from django.urls import path
from . import views

app_name = 'surveys'

# Web URLs (только веб-интерфейс)
urlpatterns = [
    # Веб-интерфейс
    path('', views.SurveyListView.as_view(), name='survey_list'),
    path('survey/<slug:slug>/', views.SurveyDetailView.as_view(), name='survey_detail'),
    path('survey/<slug:slug>/embed/', views.survey_embed_view, name='survey_embed'),
    
    # Аутентификация NII EDU
    path('survey/<slug:slug>/login/', views.niiedu_login_view, name='niiedu_login'),
    path('survey/<slug:slug>/logout/', views.niiedu_logout_view, name='niiedu_logout'),
] 