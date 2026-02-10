"""
Tests for the analyzer app.

Covers ML pipeline, text processing, skill extraction, forms, and views.
"""
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock

from .ml.text_processing import clean_text
from .ml.skills import extract_skills, SKILL_VOCABULARY
from .ml.pipeline import ResumeMatcher
from .forms import ResumeAnalysisForm
from .models import AnalysisResult


class CleanTextTest(TestCase):
    """Tests for the text cleaning/normalization function."""

    def test_lowercasing(self):
        self.assertEqual(clean_text("HELLO WORLD"), "hello world")

    def test_whitespace_normalization(self):
        self.assertEqual(clean_text("hello   \n\t  world"), "hello world")

    def test_empty_string(self):
        self.assertEqual(clean_text(""), "")

    def test_none_input(self):
        self.assertEqual(clean_text(None), "")

    def test_preserves_special_chars(self):
        result = clean_text("C++ and C# developer")
        self.assertIn("c++", result)
        self.assertIn("c#", result)


class SkillExtractionTest(TestCase):
    """Tests for skill extraction from text."""

    def test_extracts_known_skills(self):
        text = "Experience with Python, Django, and PostgreSQL"
        skills = extract_skills(text)
        self.assertIn("python", skills)
        self.assertIn("django", skills)
        self.assertIn("postgresql", skills)

    def test_returns_empty_for_no_skills(self):
        text = "I enjoy hiking and cooking"
        skills = extract_skills(text)
        self.assertEqual(skills, [])

    def test_returns_empty_for_empty_text(self):
        skills = extract_skills("")
        self.assertEqual(skills, [])

    def test_no_partial_matches(self):
        # "angular" should not match inside "rectangular"
        text = "rectangular shapes"
        skills = extract_skills(text)
        self.assertNotIn("angular", skills)

    def test_custom_vocabulary(self):
        custom = ["wizardry", "alchemy"]
        text = "Expert in wizardry and alchemy"
        skills = extract_skills(text, vocabulary=custom)
        self.assertIn("wizardry", skills)
        self.assertIn("alchemy", skills)

    def test_results_are_sorted(self):
        text = "Python, Java, AWS, Django"
        skills = extract_skills(text)
        self.assertEqual(skills, sorted(skills))


class ResumeMatcherTest(TestCase):
    """Tests for the TF-IDF + cosine similarity pipeline."""

    def setUp(self):
        self.matcher = ResumeMatcher()

    def test_identical_texts_high_similarity(self):
        text = "Senior Python developer with Django experience"
        score = self.matcher.compute_similarity(text, text)
        self.assertGreater(score, 0.9)

    def test_different_texts_lower_similarity(self):
        resume = "Python developer with Django and REST API experience"
        job = "Marketing manager with social media expertise"
        score = self.matcher.compute_similarity(resume, job)
        self.assertLess(score, 0.3)

    def test_empty_texts_return_zero(self):
        self.assertEqual(self.matcher.compute_similarity("", "some text"), 0.0)
        self.assertEqual(self.matcher.compute_similarity("some text", ""), 0.0)

    def test_analyze_returns_all_keys(self):
        result = self.matcher.analyze(
            "Python developer skilled in Django and machine learning",
            "Looking for Python developer with Django and AWS experience"
        )
        expected_keys = {
            'similarity_score', 'match_percentage',
            'resume_skills', 'job_skills', 'missing_skills'
        }
        self.assertEqual(set(result.keys()), expected_keys)

    def test_analyze_missing_skills(self):
        result = self.matcher.analyze(
            "Python developer skilled in Django",
            "Looking for Python developer with Django and AWS experience"
        )
        self.assertIn("aws", result['missing_skills'])

    def test_singleton_pattern(self):
        matcher1 = ResumeMatcher()
        matcher2 = ResumeMatcher()
        self.assertIs(matcher1, matcher2)


class ResumeAnalysisFormTest(TestCase):
    """Tests for form validation."""

    def test_valid_form(self):
        pdf_content = b'%PDF-1.4 test content with enough data'
        file = SimpleUploadedFile("resume.pdf", pdf_content, content_type="application/pdf")
        form = ResumeAnalysisForm(
            data={'job_description': 'A' * 60},
            files={'resume_file': file}
        )
        self.assertTrue(form.is_valid())

    def test_rejects_non_pdf(self):
        file = SimpleUploadedFile("resume.txt", b"text content", content_type="text/plain")
        form = ResumeAnalysisForm(
            data={'job_description': 'A' * 60},
            files={'resume_file': file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('resume_file', form.errors)

    def test_rejects_short_job_description(self):
        pdf_content = b'%PDF-1.4 test content'
        file = SimpleUploadedFile("resume.pdf", pdf_content, content_type="application/pdf")
        form = ResumeAnalysisForm(
            data={'job_description': 'Too short'},
            files={'resume_file': file}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('job_description', form.errors)

    def test_rejects_missing_file(self):
        form = ResumeAnalysisForm(
            data={'job_description': 'A' * 60},
            files={}
        )
        self.assertFalse(form.is_valid())
        self.assertIn('resume_file', form.errors)


class ViewTests(TestCase):
    """Tests for view status codes and templates."""

    def setUp(self):
        self.client = Client()

    def test_upload_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyzer/upload.html')

    def test_history_page_loads(self):
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyzer/history.html')

    def test_results_page_404_for_missing(self):
        response = self.client.get('/results/9999/')
        self.assertEqual(response.status_code, 404)

    def test_results_page_with_data(self):
        analysis = AnalysisResult.objects.create(
            resume_file='test.pdf',
            job_description='Test job description',
            similarity_score=0.75,
            match_percentage=75.0,
            resume_skills=['python', 'django'],
            job_skills=['python', 'django', 'aws'],
            missing_skills=['aws'],
        )
        response = self.client.get(f'/results/{analysis.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analyzer/results.html')

    def test_health_check(self):
        """Test the health check endpoint returns 200 OK."""
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})


class AnalysisResultModelTest(TestCase):
    """Tests for the AnalysisResult model."""

    def test_score_label_excellent(self):
        obj = AnalysisResult(match_percentage=85)
        self.assertEqual(obj.score_label, 'Excellent')

    def test_score_label_good(self):
        obj = AnalysisResult(match_percentage=65)
        self.assertEqual(obj.score_label, 'Good')

    def test_score_label_fair(self):
        obj = AnalysisResult(match_percentage=45)
        self.assertEqual(obj.score_label, 'Fair')

    def test_score_label_low(self):
        obj = AnalysisResult(match_percentage=25)
        self.assertEqual(obj.score_label, 'Low')

    def test_score_label_very_low(self):
        obj = AnalysisResult(match_percentage=10)
        self.assertEqual(obj.score_label, 'Very Low')

    def test_score_color(self):
        obj = AnalysisResult(match_percentage=85)
        self.assertEqual(obj.score_color, 'score-excellent')
