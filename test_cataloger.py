#!/usr/bin/env python3
"""
Test script for the document cataloger
"""

from document_cataloger import DocumentCataloguer
from pathlib import Path

def test_cataloger():
    print("Testing Document Cataloger Components")
    print("=" * 40)
    
    # Initialize cataloguer
    kb_path = "."
    cataloguer = DocumentCataloguer(kb_path)
    
    # Find a test file
    test_files = list(Path('.').glob('**/*.pdf'))[:1]
    if not test_files:
        print("No PDF files found for testing")
        return
    
    test_file = test_files[0]
    print(f"Testing with: {test_file.name}")
    
    try:
        # Test text extraction
        text = cataloguer.extract_text_from_pdf(test_file)
        print(f"✓ Text extraction: {len(text)} characters extracted")
        
        # Test sector detection
        sector = cataloguer.determine_sector(test_file)
        print(f"✓ Sector detection: {sector}")
        
        # Test fallback metadata
        metadata = cataloguer.get_fallback_metadata(test_file)
        print(f"✓ Fallback metadata: {metadata['title']}")
        
        # Test doc_id generation
        doc_id = cataloguer.generate_doc_id(sector, 'standard', 'Test Pub', 'Test Doc', '2023')
        print(f"✓ Doc ID generation: {doc_id}")
        
        # Test checksum
        checksum = cataloguer.get_file_checksum(test_file)
        print(f"✓ Checksum: {checksum[:16]}...")
        
        print("\n✅ All core components working!")
        print("\nTo run full cataloging:")
        print("python3 document_cataloger.py --test")
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cataloger()