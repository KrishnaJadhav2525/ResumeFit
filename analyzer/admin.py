"""
Admin configuration for the analyzer app.
"""
from django.contrib import admin
from .models import AnalysisResult


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'match_percentage', 'score_label', 'created_at')
    list_filter = ('created_at',)
    readonly_fields = (
        'similarity_score', 'match_percentage',
        'resume_skills', 'job_skills', 'missing_skills',
        'created_at',
    )
    ordering = ('-created_at',)
