"""
Text processing utilities for resume analysis.

Handles PDF text extraction (via PyMuPDF) and text cleaning/normalization.
"""
import re
import fitz  # PyMuPDF


def extract_text_from_pdf(file_obj):
    """
    Extract text content from an uploaded PDF file.

    Args:
        file_obj: A Django UploadedFile (or any file-like object with .read()).

    Returns:
        str: Extracted text from all pages of the PDF.

    Raises:
        ValueError: If the PDF cannot be read or contains no extractable text.
    """
    try:
        pdf_bytes = file_obj.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())

        doc.close()
        full_text = "\n".join(text_parts)

        if not full_text.strip():
            raise ValueError(
                "The PDF appears to contain no extractable text. "
                "It may be a scanned image. Please upload a text-based PDF."
            )

        return full_text

    except fitz.fitz.FileDataError:
        raise ValueError("The uploaded file is not a valid PDF or is corrupted.")
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Failed to process PDF: {str(e)}")


def clean_text(text):
    """
    Clean and normalize extracted text for NLP processing.

    Steps:
        1. Convert to lowercase
        2. Replace newlines/tabs with spaces
        3. Remove non-alphanumeric characters (keep spaces)
        4. Collapse multiple spaces into one
        5. Strip leading/trailing whitespace

    Args:
        text (str): Raw text to clean.

    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Replace newlines and tabs with spaces
    text = text.replace('\n', ' ').replace('\t', ' ')

    # Remove special characters but keep letters, digits, and spaces
    text = re.sub(r'[^a-z0-9\s\+\#\.]', ' ', text)

    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
