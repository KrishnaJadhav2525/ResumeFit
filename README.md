# ResumeFit

**Resume–Job Description Matching** powered by real machine learning — TF-IDF vectorization and cosine similarity via scikit-learn.

No GPT. No LLMs. No paid APIs. Just honest, explainable NLP.

---

## Features

- **PDF Resume Upload** — Text extraction via PyMuPDF with file type/size validation
- **TF-IDF + Cosine Similarity** — Statistical matching score (0–100%) between resume and job description
- **Skill Extraction** — 100+ skill vocabulary with word-boundary-aware regex matching
- **Gap Analysis** — Identifies skills required by the job but missing from your resume
- **Analysis History** — All results persisted to database with timestamped history view
- **Premium Dark UI** — Responsive design with gradient accents, glassmorphism, and micro-animations

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 |
| ML / NLP | scikit-learn (TF-IDF, cosine similarity) |
| PDF Processing | PyMuPDF (fitz) |
| Static Files | WhiteNoise |
| WSGI Server | Gunicorn |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Deployment | Railway / Render compatible |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/KrishnaJadhav2525/ResumeFit.git
cd ResumeFit

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## Project Structure

```
ResumeFit/
├── manage.py
├── requirements.txt
├── Procfile                        # Deployment process config
├── build.sh                        # Deploy build script
├── resumefit/                      # Django project settings
│   ├── settings.py                 # Production-safe configuration
│   ├── urls.py
│   └── wsgi.py
├── analyzer/                       # Main Django application
│   ├── models.py                   # AnalysisResult model (JSONField for skills)
│   ├── forms.py                    # Upload validation (PDF type, size, min length)
│   ├── views.py                    # Upload, results, and history views
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py                    # 31 tests
│   ├── ml/                         # ← ML pipeline (isolated module)
│   │   ├── pipeline.py             # Singleton TF-IDF vectorizer + cosine similarity
│   │   ├── skills.py               # Editable skill vocabulary + extraction
│   │   └── text_processing.py      # PDF text extraction + cleaning
│   └── templates/analyzer/
│       ├── base.html               # Dark-mode base layout
│       ├── upload.html             # Upload form with drag-and-drop
│       ├── results.html            # Score ring, skill cards, transparency note
│       └── history.html            # Past analyses table
└── static/css/
    └── style.css                   # Complete design system (CSS custom properties)
```

---

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| **TF-IDF + Cosine Similarity** | Simple, proven approach for document similarity. No training data needed — works on any resume/JD pair immediately. |
| **Singleton Vectorizer** | The `ResumeMatcher` class uses `__new__` to ensure the TF-IDF vectorizer is initialized once, not re-created per request. |
| **Skill Vocabulary File** | Skills are matched via a predefined list in `skills.py` rather than NER or entity extraction. This is transparent, editable, and produces zero false positives from model hallucination. |
| **No Pre-trained Models** | We don't ship any model files. TF-IDF is computed per comparison from the two input documents. This keeps the deployment footprint small. |
| **JSONField for Skills** | Storing extracted skills as JSON arrays in the database avoids complex many-to-many tables for a feature that's read-heavy and rarely queried by individual skill. |
| **Django Forms (not DRF)** | The app is server-rendered with Django templates. No SPA, no REST API overhead. This is the simplest architecture that works for the use case. |

---

## Limitations & Future Improvements

### Current Limitations

- **No semantic understanding** — TF-IDF measures word overlap, not meaning. "Software Engineer" and "Developer" are treated as different terms.
- **Skill extraction is vocabulary-bound** — Only skills in the predefined list (`skills.py`) are detected. Uncommon or niche skills may be missed.
- **No OCR support** — Scanned PDF resumes (image-based) cannot be processed. Only text-based PDFs are supported.
- **Single-language** — English only. No internationalization of skill matching.
- **No user accounts** — All analyses are visible to all visitors. No authentication layer.

### Possible Improvements (without scope creep)

- Add user authentication for private analysis history
- Implement synonym mapping (e.g., "JS" → "JavaScript") for better skill matching
- Add a confidence indicator explaining what drove the score
- Support DOCX uploads in addition to PDF
- Add basic result export (PDF report or CSV)

---

## Deployment

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | **Yes** (prod) | dev fallback | Django secret key |
| `DJANGO_DEBUG` | No | `True` | Set to `False` in production |
| `DJANGO_ALLOWED_HOSTS` | No | `localhost,127.0.0.1` | Comma-separated hostnames |
| `DATABASE_URL` | No | SQLite | PostgreSQL connection string |
| `CSRF_TRUSTED_ORIGINS` | No | localhost URLs | Comma-separated HTTPS origins |
| `SECURE_SSL_REDIRECT` | No | `True` | Disable if behind a reverse proxy handling SSL |
| `LOG_LEVEL` | No | `WARNING` | Root log level (`DEBUG`, `INFO`, etc.) |

### Deploy to Railway

1. Connect your GitHub repo to [Railway](https://railway.app)
2. Add a PostgreSQL plugin
3. Set environment variables (above)
4. Railway auto-detects the `Procfile` and deploys

### Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repo
3. Set **Build Command**: `bash build.sh`
4. Set **Start Command**: `gunicorn resumefit.wsgi --log-file -`
5. Add environment variables
6. Add a PostgreSQL database

---

## Tests

```bash
python manage.py test analyzer -v 2
```

**31 tests** covering:
- Text cleaning and normalization
- Skill extraction (boundary matching, custom vocabulary)
- TF-IDF pipeline (similarity scores, edge cases, singleton)
- Form validation (file type, size, min description length)
- View responses (status codes, templates)
- Model properties (score labels, color classes)

---

## Honesty Statement

This project uses **TF-IDF vectorization** and **cosine similarity** — established, well-understood NLP techniques from scikit-learn. The skill extraction uses **keyword matching** against a predefined vocabulary.

This is not:
- ❌ "AI-powered" in the marketing sense
- ❌ GPT, LLM, or neural network based
- ❌ A black-box system

It **is**:
- ✅ Real machine learning (statistical NLP)
- ✅ Fully explainable and verifiable
- ✅ Open-source, local, and free to run

---

## License

MIT
