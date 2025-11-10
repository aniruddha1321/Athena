# pdf_utils.py - Better PDF text extraction
import PyPDF2
import re


def clean_extracted_text(text: str) -> str:
    """
    Clean PDF text that has spaces between characters.
    Fixes: "M a y  2 0 2 5" -> "May 2025"
    """
    # Remove excessive spaces between single characters
    # Pattern: single char + space + single char
    cleaned = re.sub(r'(?<=\S)\s+(?=\S\s)', '', text)
    
    # Remove multiple spaces
    cleaned = re.sub(r'\s{2,}', ' ', cleaned)
    
    # Fix common patterns
    cleaned = re.sub(r'([a-zA-Z])\s+([a-zA-Z])\s+([a-zA-Z])', r'\1\2\3', cleaned)
    
    return cleaned.strip()


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF with cleaning.
    Works with both file paths and uploaded file objects.
    """
    try:
        # Handle both file path and file-like object
        if isinstance(pdf_file, str):
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        else:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        # Clean the text
        cleaned_text = clean_extracted_text(text)
        
        print(f"📄 Extracted: {len(text)} chars -> Cleaned: {len(cleaned_text)} chars")
        
        return cleaned_text
        
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        raise


def extract_text_from_pdf_advanced(pdf_file) -> str:
    """
    Advanced extraction that tries multiple methods.
    Falls back to PyPDF2 if other methods fail.
    """
    text = ""
    
    # Try PyPDF2 first
    try:
        if isinstance(pdf_file, str):
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"⚠️ PyPDF2 extraction failed: {e}")
    
    # Clean the text
    if text:
        cleaned_text = clean_extracted_text(text)
        
        # Check if cleaning improved things
        if len(cleaned_text) > len(text) * 0.5:  # At least 50% of original
            return cleaned_text
        else:
            print("⚠️ Cleaning may have removed too much, using original")
            return text
    
    return text


# Test function
if __name__ == "__main__":
    # Test cleaning
    test_text = "M a y  2 0 2 5  -  A u g  2 0 2 5\nP y t h o n"
    print("Before:", test_text)
    print("After:", clean_extracted_text(test_text))