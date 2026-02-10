"""
Forms for the analyzer app.

Handles validation for resume uploads and job description input.
"""
from django import forms


class ResumeAnalysisForm(forms.Form):
    """
    Form for submitting a resume PDF and job description for analysis.

    Validation rules:
        - resume_file: Must be a PDF, max 5 MB
        - job_description: Minimum 50 characters
    """
    resume_file = forms.FileField(
        label='Upload Resume (PDF)',
        help_text='PDF format only. Maximum file size: 5 MB.',
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf,application/pdf',
            'class': 'form-input file-input',
            'id': 'resume-file-input',
        }),
    )

    job_description = forms.CharField(
        label='Job Description',
        help_text='Paste the full job description here (minimum 50 characters).',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'placeholder': 'Paste the job description here...\n\n'
                           'Include responsibilities, requirements, and preferred qualifications '
                           'for the best matching results.',
            'class': 'form-input textarea-input',
            'id': 'job-description-input',
        }),
    )

    def clean_resume_file(self):
        """Validate that the uploaded file is a PDF and within size limits."""
        file = self.cleaned_data.get('resume_file')
        if file:
            # Check file extension
            if not file.name.lower().endswith('.pdf'):
                raise forms.ValidationError(
                    'Only PDF files are accepted. Please upload a .pdf file.'
                )

            # Check content type
            if file.content_type not in ('application/pdf', 'application/x-pdf'):
                raise forms.ValidationError(
                    'Invalid file type. Please upload a valid PDF document.'
                )

            # Check file size (5 MB limit)
            max_size = 5 * 1024 * 1024  # 5 MB
            if file.size > max_size:
                raise forms.ValidationError(
                    f'File size exceeds 5 MB limit. '
                    f'Your file is {file.size / (1024 * 1024):.1f} MB.'
                )

        return file

    def clean_job_description(self):
        """Validate minimum content length for meaningful analysis."""
        text = self.cleaned_data.get('job_description', '').strip()

        if len(text) < 50:
            raise forms.ValidationError(
                f'Job description is too short ({len(text)} characters). '
                f'Please provide at least 50 characters for meaningful analysis.'
            )

        return text
