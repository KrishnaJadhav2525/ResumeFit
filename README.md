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

## 🏗 Architecture

```mermaid
graph TD
    User[User] -->|Upload PDF| Form[Django Form]
    Form -->|Validate| Clean[Text Cleaning]
    Clean -->|Raw Text| Singleton[ResumeMatcher (Singleton)]
    
    subgraph "ML Pipeline (scikit-learn)"
        Singleton -->|Fit/Transform| TFIDF[TF-IDF Vectorizer]
        TFIDF -->|Vectors| Cosine[Cosine Similarity]
        Cosine -->|Score 0-1.0| Result
    end
    
    subgraph "Skill Extraction"
        Clean -->|Regex| Extractor[Skill Extractor]
        Extractor -->|Match Vocabulary| Skills[Identified Skills]
    end
    
    Result --> DB[(PostgreSQL/SQLite)]
    Skills --> DB
    DB --> View[Results View]
```

## 🧠 Deep Dive: Why TF-IDF?

We chose **TF-IDF (Term Frequency-Inverse Document Frequency)** over complex LLM embeddings for three reasons:

1.  **Explainability**: We can tell you exactly *which* words contributed to the match. Embeddings are black boxes.
2.  **Speed**: It runs in milliseconds on a single CPU core. No GPU required.
3.  **Deterministic**: The same resume + job description always yields the same score.

**The Math:**
-   **TF**: How often a word appears in the resume.
-   **IDF**: How rare the word is across the "corpus" (here, the two documents).
-   **Cosine Similarity**: Measures the angle between the two text vectors. 
    -   Angle = 0° (Match) → Cosine = 1.0
    -   Angle = 90° (No overlap) → Cosine = 0.0

---

## 🛠 Tech Stack

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
