#!/usr/bin/env python3
"""
Quick test to verify PDF cleaning works
"""

from pdf_utils import extract_text_from_pdf, clean_extracted_text
from semantic_search import build_semantic_index, search_semantic

# Your resume path
pdf_path = "Sagar Prajapati Resume Final Nov .pdf (2).pdf"

print("=" * 70)
print("🔧 TESTING PDF CLEANING FIX")
print("=" * 70)

# Step 1: Test the cleaning function directly
print("\n1️⃣ Testing text cleaning function:")
test_text = "M a y  2 0 2 5  -  A u g  2 0 2 5\nG e e k s f o r G e e k s\n5 4 0  p r o b l e m s"
print(f"Before: {test_text}")
cleaned = clean_extracted_text(test_text)
print(f"After:  {cleaned}")

# Step 2: Extract and clean the actual PDF
print("\n2️⃣ Extracting PDF with new cleaning:")
try:
    text = extract_text_from_pdf(pdf_path)
    print(f"\n✅ Extracted {len(text)} characters")
    print(f"\n📝 First 300 characters:")
    print(text[:300])
    
    # Check if specific terms are now readable
    print("\n3️⃣ Checking for key terms:")
    terms = ["GeeksforGeeks", "540", "Python", "May 2025", "COEP"]
    for term in terms:
        if term in text:
            print(f"   ✅ Found: {term}")
        else:
            # Try case-insensitive
            if term.lower() in text.lower():
                print(f"   ✅ Found (case-insensitive): {term}")
            else:
                print(f"   ❌ Missing: {term}")
    
    # Step 3: Test semantic search with cleaned text
    print("\n4️⃣ Testing semantic search with cleaned text:")
    vectordb = build_semantic_index(text, chunk_size=500, chunk_overlap=100)
    
    test_queries = [
        "GeeksforGeeks problems",
        "540 DSA problems",
        "Python programming skills",
        "work experience COEP"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = search_semantic(vectordb, query, k=3)
        
        if results:
            # Show top result
            top_text, top_distance = results[0]
            print(f"   ✅ Top match (distance={top_distance:.4f}):")
            print(f"   {top_text[:150]}...")
        else:
            print(f"   ❌ No results")
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE - If you see readable text above, the fix works!")
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()