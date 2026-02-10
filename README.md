# ResumeFit

A Django application that performs resume analysis and job matching using **real machine learning** — TF-IDF vectorization and cosine similarity via scikit-learn.

## Features

- **Resume Upload**: Upload PDF resumes for text extraction (PyMuPDF)
- **Job Matching**: TF-IDF + cosine similarity scoring against job descriptions
- **Skill Extraction**: Keyword-based skill matching against a vocabulary of 100+ skills
- **Gap Analysis**: Identifies missing skills between resume and job requirements
- **Analysis History**: All results stored in database and viewable in history

## Tech Stack

- **Backend**: Django 4.2
- **ML**: scikit-learn (TF-IDF, cosine similarity)
- **PDF Processing**: PyMuPDF
- **Static Files**: WhiteNoise
- **Database**: SQLite (dev) / PostgreSQL (prod)

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deployment

Configured for Railway / Render. Set these environment variables:

```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgres://...
CSRF_TRUSTED_ORIGINS=https://your-domain.com
```

## Honesty Note

This system uses **TF-IDF vectorization** and **cosine similarity** — real, explainable machine learning techniques. It does not use GPT, LLMs, or any paid AI services. Results are statistical and should supplement, not replace, human judgment.
