"""
Admin configuration for the analyzer app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'resume_filename',
        'display_score',
        'skill_count',
        'resume_skill_count',
        'missing_skill_count',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = ('resume_file', 'job_description')
    readonly_fields = (
        'resume_file',
        'job_description',
        'similarity_score',
        'resume_skills',
        'job_skills',
        'missing_skills',
        'created_at',
    )
    ordering = ('-created_at',)

    fieldsets = (
        ('Overview', {
            'fields': (
                ('similarity_score', 'created_at'),
            ),
        }),
        ('Missing Skills', {
            'fields': ('missing_skills',),
            'classes': ('collapse',),
            'description': 'Skills present in Job Description but missing from Resume.',
        }),
        ('Extracted Data', {
            'fields': ('resume_skills', 'job_skills'),
            'classes': ('collapse',),
        }),
        ('Source Content', {
            'fields': ('resume_file', 'job_description'),
            'classes': ('collapse',),
        }),
    )

    def resume_filename(self, obj):
        return obj.resume_file.name.split('/')[-1]
    resume_filename.short_description = 'Resume File'

    def display_score(self, obj):
        color = obj.score_color
        # Map bootstrap classes to hex colors for admin
        hex_map = {
            'success': '#28a745',  # Green
            'info': '#17a2b8',     # Teal
            'warning': '#ffc107',  # Yellow/Orange
            'danger': '#dc3545',   # Red
        }
        hex_color = hex_map.get(color, '#6c757d')
        
        return format_html(
            '<b style="color: {};">{}%</b>',
            hex_color,
            round(obj.similarity_score * 100, 1)
        )
    display_score.short_description = 'Match Score'
    display_score.admin_order_field = 'similarity_score'

    def skill_count(self, obj):
        return len(obj.job_skills)
    skill_count.short_description = 'Job Skills'

    def resume_skill_count(self, obj):
        return len(obj.resume_skills)
    resume_skill_count.short_description = 'Resume Skills'

    def missing_skill_count(self, obj):
        return len(obj.missing_skills)
    missing_skill_count.short_description = 'Missing'
