#!/usr/bin/env python3
"""
Test script for incremental cataloging functionality
"""

from document_cataloger import DocumentCataloguer
from pathlib import Path
import shutil
import tempfile

def test_incremental_features():
    print("Testing Incremental Cataloging Features")
    print("=" * 45)
    
    cataloguer = DocumentCataloguer(".")
    
    print("1. Testing change detection...")
    
    # Scan for changes
    new_files, deleted_files = cataloguer.scan_for_file_changes()
    
    print(f"   New files found: {len(new_files)}")
    for f in new_files[:3]:  # Show first 3
        print(f"   - {f.name}")
    if len(new_files) > 3:
        print(f"   ... and {len(new_files) - 3} more")
    
    print(f"   Deleted files: {len(deleted_files)}")
    for f in deleted_files[:3]:  # Show first 3
        print(f"   - {f}")
    if len(deleted_files) > 3:
        print(f"   ... and {len(deleted_files) - 3} more")
    
    print(f"\n2. Current catalog status:")
    print(f"   Total existing entries: {len(cataloguer.existing_catalog)}")
    
    if new_files or deleted_files:
        print(f"   ⚠️  Changes detected - catalog needs updating")
    else:
        print(f"   ✅ Catalog is up to date")
    
    print(f"\n3. Sample existing entries:")
    for i, (file_path, entry) in enumerate(list(cataloguer.existing_catalog.items())[:3]):
        doc_id = entry.get('doc_id', 'Unknown')
        title = entry.get('title', 'Unknown')
        print(f"   {i+1}. {doc_id}: {title}")
    
    print(f"\nTo run incremental update:")
    print(f"   ./run_cataloger.sh                  # Default incremental mode")
    print(f"   python3 document_cataloger.py       # Same as above")
    print(f"   python3 document_cataloger.py --full # Full reprocessing")

if __name__ == "__main__":
    test_incremental_features()