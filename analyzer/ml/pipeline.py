"""
ML pipeline for resume–job description matching.

Uses TF-IDF vectorization and cosine similarity from scikit-learn.
The vectorizer is initialized once (singleton pattern) to avoid
re-initialization on every request.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .text_processing import clean_text
from .skills import extract_skills


class ResumeMatcher:
    """
    Singleton-style resume–job matching engine.

    The TF-IDF vectorizer is created once and reused across requests.
    This class is NOT retrained per request — it uses the vectorizer's
    fit_transform on each pair of documents to compute similarity.

    This is intentional: with only two documents per comparison,
    there is no corpus to pre-train on. The TF-IDF weights are computed
    relative to the resume and job description being compared.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._vectorizer = TfidfVectorizer(
                stop_words='english',
                max_features=5000,
                ngram_range=(1, 2),   # Unigrams + bigrams for better matching
                sublinear_tf=True,    # Apply log normalization to term frequency
            )
        return cls._instance

    @property
    def vectorizer(self):
        return self._vectorizer

    def compute_similarity(self, resume_text, job_text):
        """
        Compute cosine similarity between resume and job description.

        Args:
            resume_text (str): Cleaned resume text.
            job_text (str): Cleaned job description text.

        Returns:
            float: Cosine similarity score between 0.0 and 1.0.
        """
        if not resume_text or not job_text:
            return 0.0

        tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return round(float(similarity[0][0]), 4)

    def analyze(self, resume_text_raw, job_text_raw):
        """
        Run the full analysis pipeline.

        Args:
            resume_text_raw (str): Raw text extracted from the resume PDF.
            job_text_raw (str): Raw job description text from user input.

        Returns:
            dict: Analysis results containing:
                - similarity_score (float): 0.0 to 1.0
                - resume_skills (list[str]): Skills found in resume
                - job_skills (list[str]): Skills found in job description
                - missing_skills (list[str]): Skills in job but not in resume
                - match_percentage (float): Score as percentage (0–100)
        """
        # Clean text for vectorization
        clean_resume = clean_text(resume_text_raw)
        clean_job = clean_text(job_text_raw)

        # Compute similarity
        similarity_score = self.compute_similarity(clean_resume, clean_job)

        # Extract skills from raw text (before aggressive cleaning)
        resume_skills = extract_skills(resume_text_raw)
        job_skills = extract_skills(job_text_raw)

        # Identify missing skills (in job but not in resume)
        missing_skills = sorted(set(job_skills) - set(resume_skills))

        return {
            'similarity_score': similarity_score,
            'match_percentage': round(similarity_score * 100, 1),
            'resume_skills': resume_skills,
            'job_skills': job_skills,
            'missing_skills': missing_skills,
        }


# Module-level singleton instance — import this in views
matcher = ResumeMatcher()
