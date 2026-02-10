"""
Views for the analyzer app.

Handles resume upload, analysis execution, results display, and history.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ResumeAnalysisForm
from .models import AnalysisResult
from .ml.text_processing import extract_text_from_pdf
from .ml.pipeline import matcher


def upload_resume(request):
    """
    Main page: displays the upload form and handles analysis submission.

    GET: Shows the empty form.
    POST: Validates input, extracts PDF text, runs ML pipeline,
          saves results to DB, and redirects to results page.
    """
    if request.method == 'POST':
        form = ResumeAnalysisForm(request.POST, request.FILES)

        if form.is_valid():
            resume_file = form.cleaned_data['resume_file']
            job_description = form.cleaned_data['job_description']

            try:
                # Step 1: Extract text from PDF
                resume_text = extract_text_from_pdf(resume_file)

                # Reset file pointer so Django can save the file
                resume_file.seek(0)

                # Step 2: Run the ML analysis pipeline
                results = matcher.analyze(resume_text, job_description)

                # Step 3: Save results to database
                analysis = AnalysisResult.objects.create(
                    resume_file=resume_file,
                    job_description=job_description,
                    similarity_score=results['similarity_score'],
                    match_percentage=results['match_percentage'],
                    resume_skills=results['resume_skills'],
                    job_skills=results['job_skills'],
                    missing_skills=results['missing_skills'],
                )

                messages.success(request, 'Analysis complete!')
                return redirect('analyzer:results', pk=analysis.pk)

            except ValueError as e:
                # PDF extraction errors
                messages.error(request, str(e))
            except Exception as e:
                messages.error(
                    request,
                    'An unexpected error occurred during analysis. Please try again.'
                )
    else:
        form = ResumeAnalysisForm()

    # Show recent analyses on the upload page
    recent_analyses = AnalysisResult.objects.all()[:5]

    return render(request, 'analyzer/upload.html', {
        'form': form,
        'recent_analyses': recent_analyses,
    })


def view_results(request, pk):
    """
    Display the results of a specific analysis.
    """
    analysis = get_object_or_404(AnalysisResult, pk=pk)

    # Calculate common skills (in both resume and JD)
    common_skills = sorted(
        set(analysis.resume_skills) & set(analysis.job_skills)
    )

    # Resume-only skills (in resume but not required by JD)
    extra_skills = sorted(
        set(analysis.resume_skills) - set(analysis.job_skills)
    )

    return render(request, 'analyzer/results.html', {
        'analysis': analysis,
        'common_skills': common_skills,
        'extra_skills': extra_skills,
    })


def analysis_history(request):
    """
    Display a list of all past analyses, ordered by most recent first.
    """
    analyses = AnalysisResult.objects.all()

    return render(request, 'analyzer/history.html', {
        'analyses': analyses,
    })


def health_check(request):
    """
    Simple health check endpoint returning 200 OK.
    Used by hosting platforms to verify the app is up.
    """
    from django.http import JsonResponse
    return JsonResponse({'status': 'ok'}, status=200)
