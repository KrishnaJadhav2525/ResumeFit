"""
Skill extraction module.

Uses a predefined, editable skill vocabulary to identify
skills in resume and job description text via keyword matching.
"""
import re

# ---------------------------------------------------------------------------
# Predefined skill vocabulary — EDITABLE
#
# Add or remove skills here. Each skill should be lowercase.
# Multi-word skills are supported (e.g., "machine learning").
# ---------------------------------------------------------------------------
SKILL_VOCABULARY = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby",
    "go", "rust", "swift", "kotlin", "php", "scala", "r", "matlab",
    "perl", "bash", "shell scripting", "sql", "html", "css",

    # Web Frameworks & Libraries
    "django", "flask", "fastapi", "react", "angular", "vue.js", "node.js",
    "express.js", "spring boot", "ruby on rails", "asp.net", "next.js",
    "svelte", "jquery", "bootstrap", "tailwind css",

    # Data Science & ML
    "machine learning", "deep learning", "natural language processing",
    "computer vision", "data analysis", "data visualization",
    "scikit-learn", "tensorflow", "pytorch", "keras", "pandas", "numpy",
    "scipy", "matplotlib", "seaborn", "opencv", "nltk", "spacy",
    "data mining", "statistical modeling", "feature engineering",

    # Databases
    "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "sqlite", "oracle", "sql server", "cassandra", "dynamodb",
    "firebase", "neo4j",

    # Cloud & DevOps
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "terraform", "ansible", "jenkins", "ci/cd", "github actions",
    "gitlab ci", "linux", "nginx", "apache",

    # Tools & Platforms
    "git", "github", "gitlab", "bitbucket", "jira", "confluence",
    "slack", "figma", "postman", "swagger", "graphql", "rest api",
    "microservices", "serverless",

    # Data Engineering
    "apache spark", "hadoop", "kafka", "airflow", "etl",
    "data warehousing", "snowflake", "databricks",

    # Testing
    "unit testing", "integration testing", "selenium", "pytest",
    "jest", "cypress", "test driven development",

    # Soft Skills
    "leadership", "communication", "teamwork", "problem solving",
    "critical thinking", "project management", "agile", "scrum",
    "time management", "mentoring",

    # Security
    "cybersecurity", "penetration testing", "encryption",
    "authentication", "authorization", "oauth", "jwt",

    # Mobile
    "android", "ios", "react native", "flutter",

    # Other
    "blockchain", "web scraping", "api development",
    "system design", "object oriented programming", "functional programming",
    "version control", "technical writing", "data structures",
    "algorithms", "design patterns",
]


def _normalize_for_matching(text):
    """
    Normalize text for skill matching.
    Keeps letters, digits, spaces, +, #, and dots.
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\+\#\./]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_skills(text, vocabulary=None):
    """
    Extract skills from text using keyword matching against a predefined vocabulary.

    Uses word-boundary-aware matching so that partial words are not matched
    (e.g., "angular" won't match inside "rectangular").

    Args:
        text (str): The text to search for skills (should be pre-cleaned).
        vocabulary (list, optional): Custom skill list. Defaults to SKILL_VOCABULARY.

    Returns:
        list: Sorted list of matched skill strings.
    """
    if not text:
        return []

    if vocabulary is None:
        vocabulary = SKILL_VOCABULARY

    normalized_text = _normalize_for_matching(text)
    found_skills = []

    for skill in vocabulary:
        # Escape special regex characters in skill name
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, normalized_text):
            found_skills.append(skill)

    return sorted(set(found_skills))
