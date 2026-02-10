# ResumeFit

**Resume–Job Description Matching Application**

A production-ready Django application that analyzes resume relevance using **TF-IDF vectorization** and **cosine similarity**. Built with Python, scikit-learn, and PyMuPDF.

> **Honesty Note**: This project uses traditional statistical NLP techniques. It does **not** use GPT, LLMs, or any external AI APIs. It is fast, free to run, and fully explainable.

---

## 🚀 Features

- **Text Extraction**: Robust PDF parsing via `PyMuPDF` (fitz).
- **Match Scoring**: Calculates a 0-100% similarity score based on term frequency (TF-IDF).
- **Skill Extraction**: Identifies 100+ technical and soft skills using regex pattern matching.
- **Gap Analysis**: Highlights skills required by the job but missing from the resume.
- **History Tracking**: Persists all analyses to a PostgreSQL/SQLite database.
- **Health Monitoring**: Dedicated `/health/` endpoint for uptime checks.
- **Premium UI**: Dark-mode interface with glassmorphism, responsive design, and score visualizations.

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Django 4.2 (Python 3.10+) |
| **NLP Engine** | scikit-learn (TfidfVectorizer, Cosine Similarity) |
| **PDF Tools** | PyMuPDF (fitz) |
| **Database** | PostgreSQL (Prod) / SQLite (Dev) |
| **Server** | Gunicorn + WhiteNoise (Static Files) |
| **Hosting** | Render / Railway compatible |

---

## 🧠 How It Works

1.  **Preprocessing**: Text is extracted from the uploaded PDF and the job description. It is cleaned (lowercased, normalized) to remove noise.
2.  **Vectorization**: Both texts are converted into numerical vectors using **TF-IDF** (Term Frequency-Inverse Document Frequency). This downweights common words (like "the", "and") and highlights unique, meaningful terms.
3.  **Similarity**: A **Cosine Similarity** score is calculated between the two vectors, measuring the angle between them. A higher score means the resume's content is statistically closer to the job description.
4.  **Keyword Matching**: The text is scanned against a predefined vocabulary (`skills.py`) to extract specific technical skills for the "Missing Skills" report.

---

## 📐 Design Decisions

| Decision | Rationale |
| :--- | :--- |
| **Singleton Vectorizer** | The `ResumeMatcher` class initializes the TF-IDF model once (singleton pattern) to avoid re-loading large vocabulary files on every request, ensuring low latency. |
| **JSONField for Skills** | Extracted and missing skills are stored as JSON arrays in the `AnalysisResult` model. This avoids the complexity of M2M relationships for data that is primarily read-only and display-focused. |
| **No External APIs** | By avoiding OpenAI/Anthropic APIs, the app remains free to host, private (data doesn't leave the server), and deterministic. |
| **Django Templates** | Chosen over a React/Vue SPA to keep the architecture simple and monolithic. This reduces build complexity and makes deployment straightforward. |

---

## ⚠️ Limitations

-   **Semantic Blindness**: TF-IDF matches exact words. "Coder" and "Programmer" are seen as different terms, unlike in embedding-based models.
-   **Vocabulary Bound**: Skill extraction only detects skills listed in `analyzer/ml/skills.py`.
-   **English Only**: The current tokenizer and stop-word list are optimized for English.
-   **PDF Only**: DOCX and image-based (scanned) PDFs are not currently supported.

---

## 🌍 Deployment

The application is configured for **Render** and **Railway**.

### Environment Variables
| Variable | Desciption |
| :--- | :--- |
| `DJANGO_SECRET_KEY` | Random string for cryptographic signing. |
| `DJANGO_DEBUG` | Set to `False` in production. |
| `DATABASE_URL` | PostgreSQL connection string (auto-set by Render/Railway). |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated domains (e.g., `resumefit.onrender.com`). |

### Deploy on Render
1.  Create a new **Web Service**.
2.  Connect your repository.
3.  **Build Command**: `bash build.sh`
4.  **Start Command**: `gunicorn resumefit.wsgi --log-file -`
5.  Add the environment variables above.

---

## 🛡 Health Check

The app includes a lightweight health check endpoint for monitoring services:
-   **URL**: `/health/`
-   **Response**: `{"status": "ok"}` (200 OK)

---

## 📜 License

MIT License. Open source and free to use.
