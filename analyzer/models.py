"""
Models for the analyzer app.

Stores analysis results including resume reference, job description,
similarity score, and extracted skills.
"""
from django.db import models


class AnalysisResult(models.Model):
    """
    Persists the results of a resume–job description analysis.

    Fields:
        resume_file: The uploaded PDF resume
        job_description: The job description text provided by the user
        similarity_score: Cosine similarity between resume and JD (0.0 – 1.0)
        match_percentage: Score as a percentage (0 – 100)
        resume_skills: JSON list of skills found in the resume
        job_skills: JSON list of skills found in the job description
        missing_skills: JSON list of skills in JD but not in resume
        created_at: Timestamp of analysis
    """
    resume_file = models.FileField(upload_to='resumes/%Y/%m/%d/')
    job_description = models.TextField()

    similarity_score = models.FloatField(default=0.0)
    match_percentage = models.FloatField(default=0.0)

    resume_skills = models.JSONField(default=list, blank=True)
    job_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Analysis Result'
        verbose_name_plural = 'Analysis Results'

    def __str__(self):
        return f"Analysis #{self.pk} — {self.match_percentage}% match ({self.created_at:%Y-%m-%d %H:%M})"

    @property
    def score_label(self):
        """Human-readable label for the match score."""
        if self.match_percentage >= 80:
            return 'Excellent'
        elif self.match_percentage >= 60:
            return 'Good'
        elif self.match_percentage >= 40:
            return 'Fair'
        elif self.match_percentage >= 20:
            return 'Low'
        return 'Very Low'

    @property
    def score_color(self):
        """CSS color class for the score badge."""
        if self.match_percentage >= 80:
            return 'score-excellent'
        elif self.match_percentage >= 60:
            return 'score-good'
        elif self.match_percentage >= 40:
            return 'score-fair'
        elif self.match_percentage >= 20:
            return 'score-low'
        return 'score-very-low'
