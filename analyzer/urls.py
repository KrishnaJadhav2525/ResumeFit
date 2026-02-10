"""
URL configuration for the analyzer app.
"""
from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    path('', views.upload_resume, name='upload'),
    path('results/<int:pk>/', views.view_results, name='results'),
    path('history/', views.analysis_history, name='history'),
]
