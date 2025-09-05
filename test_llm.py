#!/usr/bin/env python3
"""
Test LLM functionality for document cataloging
"""

from document_cataloger import DocumentCataloguer
from pathlib import Path

def test_llm_analysis():
    print("Testing LLM Document Analysis")
    print("=" * 40)
    
    cataloguer = DocumentCataloguer(".")
    
    # Find a test file
    test_files = list(Path('.').glob('**/*.pdf'))[:1]
    if not test_files:
        print("No PDF files found for testing")
        return
    
    test_file = test_files[0]
    print(f"Testing with: {test_file.name}")
    
    # Extract text
    text_content = cataloguer.extract_text_from_pdf(test_file)
    if not text_content:
        print("Could not extract text from PDF")
        return
    
    print(f"Extracted {len(text_content)} characters")
    print(f"First 200 chars: {text_content[:200]}...")
    
    print(f"\nTesting LLM analysis...")
    
    # Test LLM analysis
    metadata = cataloguer.analyze_document_with_llm(text_content, test_file)
    
    print(f"\nResults:")
    print(f"Title: {metadata.get('title', 'N/A')}")
    print(f"Publisher: {metadata.get('publisher', 'N/A')}")
    print(f"Year: {metadata.get('year', 'N/A')}")
    print(f"Language: {metadata.get('language', 'N/A')}")
    print(f"Summary: {metadata.get('summary', 'N/A')}")
    
    if metadata.get('summary') == "Document requires manual review for proper cataloging":
        print("\n⚠️  LLM analysis failed - using fallback metadata")
        print("This indicates an issue with the Ollama connection or prompt")
    else:
        print("\n✅ LLM analysis successful!")

if __name__ == "__main__":
    test_llm_analysis()