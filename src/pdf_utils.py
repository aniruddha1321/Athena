# pdf_utils.py - Ultimate PDF text extraction and cleaning
import PyPDF2
import re


def clean_extracted_text(text: str) -> str:
    """
    Smart cleaning for PDFs with character spacing.
    Handles: "M a y  2 0 2 5" -> "May 2025"
    Preserves: Normal word spacing
    """
    
    # Step 1: Fix character spacing aggressively
    for _ in range(15):
        text = re.sub(r'([A-Za-z0-9]) ([A-Za-z0-9])', r'\1\2', text)
    
    # Step 2: Add spaces back where needed (after punctuation, etc.)
    # Add space after period if followed by capital letter
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    
    # Add space after comma if followed by letter
    text = re.sub(r',([A-Za-z])', r', \1', text)
    
    # Add space before opening parenthesis if preceded by letter
    text = re.sub(r'([A-Za-z])\(', r'\1 (', text)
    
    # Add space after closing parenthesis if followed by letter
    text = re.sub(r'\)([A-Za-z])', r') \1', text)
    
    # Add space between lowercase and uppercase (camelCase handling)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Clean up excessive whitespace
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from PDF with aggressive cleaning.
    Works with both file paths and uploaded file objects.
    """
    try:
        # Handle both file path and file-like object
        if isinstance(pdf_file, str):
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        else:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        print(f"📄 Raw extraction: {len(text)} chars")
        print(f"🔍 Sample raw text:\n{text[:100]}")
        
        # Apply aggressive cleaning
        cleaned_text = clean_extracted_text(text)
        
        print(f"✅ After cleaning: {len(cleaned_text)} chars")
        print(f"🔍 Sample cleaned: {cleaned_text[:100]}")
        
        # Sanity check - make sure we didn't destroy the text
        if len(cleaned_text) < len(text) * 0.2:
            print("⚠️ Cleaning removed too much text, using raw version")
            return text
        
        return cleaned_text
        
    except Exception as e:
        print(f"❌ Error extracting PDF: {e}")
        raise


def extract_text_with_pdfplumber(pdf_file):
    """
    Alternative extraction using pdfplumber.
    Install: pip install pdfplumber
    """
    try:
        import pdfplumber
        
        if isinstance(pdf_file, str):
            pdf = pdfplumber.open(pdf_file)
        else:
            pdf = pdfplumber.open(pdf_file)
        
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        pdf.close()
        
        print(f"✅ PDFPlumber extracted: {len(text)} chars")
        return clean_extracted_text(text)
        
    except ImportError:
        print("⚠️ pdfplumber not installed. Using PyPDF2 instead.")
        return extract_text_from_pdf(pdf_file)
    except Exception as e:
        print(f"❌ PDFPlumber error: {e}")
        raise


# Test function
if __name__ == "__main__":
    import sys
    
    # Test the cleaning function
    test_cases = [
        ("M a y  2 0 2 5  -  A u g  2 0 2 5", "May 2025 - Aug 2025"),
        ("G e e k s f o r G e e k s", "GeeksforGeeks"),
        ("P y t h o n  p r o g r a m m i n g", "Python programming"),
        ("5 4 0  p r o b l e m s", "540 problems"),
        ("Normal text should stay", "Normal text should stay"),
    ]
    
    print("🧪 Testing Text Cleaning\n" + "="*60)
    all_passed = True
    for test_input, expected in test_cases:
        cleaned = clean_extracted_text(test_input)
        passed = cleaned == expected
        status = "✅" if passed else "❌"
        
        print(f"{status} Input:    {test_input}")
        print(f"   Expected: {expected}")
        print(f"   Got:      {cleaned}")
        print("-" * 60)
        
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All cleaning tests passed!")
    else:
        print("\n⚠️ Some tests failed - review above")
    
    # Test on actual PDF if provided
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"\n📄 Testing on: {pdf_path}")
        text = extract_text_from_pdf(pdf_path)
        print(f"\n✅ Extracted {len(text)} characters")
        print(f"\n📝 First 500 characters:\n{text[:500]}")