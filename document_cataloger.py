#!/usr/bin/env python3
"""
Document Cataloging System for Knowledge Base
Automatically extracts metadata and summarizes documents using Ollama LLM
"""

import os
import csv
import json
import hashlib
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple
import subprocess

import requests
import PyPDF2
from docx import Document as DocxDocument
import pandas as pd

class DocumentCataloguer:
    def __init__(self, knowledge_base_path: str, catalog_file: str = "00_Governance/kb_catalog.csv", 
                 ollama_url: str = "http://localhost:11434", model: str = "llama3.2:3b"):
        """
        Initialize the document cataloguer
        
        Args:
            knowledge_base_path: Path to the knowledge base root directory
            catalog_file: Relative path to the catalog CSV file
            ollama_url: URL for Ollama API
            model: Ollama model to use for document analysis
        """
        self.kb_path = Path(knowledge_base_path)
        self.catalog_path = self.kb_path / catalog_file
        self.ollama_url = ollama_url
        self.model = model
        
        # Sector mapping based on directory structure
        self.sector_mapping = {
            "01_Cross_Cutting_Standards": "Cross-Cutting",
            "02_Sector_Standards_Policies": "Mixed",
            "03_Cross_Cutting_Assessment_Guidelines_Tools": "Cross-Cutting",
            "04_Sector_Assessment_Guidelines_Tools": "Mixed",
            "05_Gold_Standard_Examples": "Mixed",
            "Health": "Health",
            "MHPSS": "MHPSS", 
            "Nutrition": "Nutrition",
            "WASH": "WASH",
            "GBV": "GBV",
            "Child_Protection": "Child Protection",
            "FSL": "FSL"
        }
        
        # Document type mapping
        self.doc_type_mapping = {
            "Standards": "standard",
            "Policies": "policy", 
            "Assessment": "assessment_tool",
            "Guidelines": "guideline",
            "Tools": "tool",
            "Examples": "example"
        }
        
        # Load existing catalog
        self.existing_catalog = self.load_existing_catalog()
        
    def load_existing_catalog(self) -> Dict[str, Dict]:
        """Load existing catalog entries to avoid reprocessing"""
        catalog_dict = {}
        if self.catalog_path.exists():
            try:
                df = pd.read_csv(self.catalog_path)
                for _, row in df.iterrows():
                    catalog_dict[row['file_path']] = row.to_dict()
            except Exception as e:
                print(f"Error loading existing catalog: {e}")
        return catalog_dict
    
    def get_file_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)
        except Exception as e:
            print(f"Error calculating checksum for {file_path}: {e}")
            return ""
        return sha256_hash.hexdigest()
    
    def extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                # Extract from first 5 pages to get metadata
                for page_num in range(min(5, len(reader.pages))):
                    text += reader.pages[page_num].extract_text()
                return text[:5000]  # Limit to first 5000 chars
        except Exception as e:
            print(f"Error extracting PDF text from {file_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(file_path)
            text = ""
            for paragraph in doc.paragraphs[:20]:  # First 20 paragraphs
                text += paragraph.text + "\n"
            return text[:5000]  # Limit to first 5000 chars
        except Exception as e:
            print(f"Error extracting DOCX text from {file_path}: {e}")
            return ""
    
    def query_ollama(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """Query Ollama API for document analysis"""
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "top_p": 0.9
                        }
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get('response', '').strip()
                else:
                    print(f"Ollama API error (attempt {attempt + 1}): {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    continue
                    
        print("Failed to get response from Ollama after all retries")
        return None
    
    def analyze_document_with_llm(self, text_content: str, file_path: Path) -> Dict[str, str]:
        """Analyze document using LLM to extract metadata and summary"""
        
        # More focused prompt with examples
        prompt = f"""You are a librarian cataloging humanitarian documents. Analyze this document excerpt and extract metadata.

Document excerpt (first 2000 characters):
{text_content[:2000]}

Extract the following information and respond ONLY with valid JSON in this exact format. ALL fields are required:
{{
    "title": "Complete document title from the text",
    "short_title": "Abbreviated version under 50 characters", 
    "publisher": "Organization that published this (WHO, UNICEF, Sphere, etc.)",
    "year": "Publication year in YYYY format",
    "language": "Language code (EN/FR/ES/AR)",
    "country_scope": "Global, Regional, or specific country name",
    "summary": "One sentence describing the document's purpose",
    "indicators_covered": "Key standards, metrics or indicators mentioned",
    "evidence_level": "normative"
}}

IMPORTANT: You must provide ALL 9 fields. If information is not clear, use these defaults:
- year: Use any year mentioned or "2023"
- country_scope: Use "Global" if not specified
- evidence_level: Use "normative" for standards/frameworks
- indicators_covered: Mention key metrics, standards, or guidelines found

Look for:
- Title in headers/covers
- Publisher logos/names (WHO, UNICEF, Sphere Project, UNHCR, etc.)
- Copyright dates or "© YYYY"
- Geographic focus mentioned in text
- Technical standards, indicators, or metrics described

Return only the JSON object, no other text."""
        
        response = self.query_ollama(prompt)
        if not response:
            print(f"No response from LLM for {file_path.name}")
            return self.get_fallback_metadata(file_path)
        
        # Debug output
        print(f"LLM response for {file_path.name}: {response[:200]}...")
            
        try:
            # Clean response - sometimes LLMs add extra text
            response = response.strip()
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                metadata = json.loads(json_str)
                
                # Validate and fill missing required fields
                required_fields = ["title", "short_title", "publisher", "year", "language", 
                                 "country_scope", "summary", "indicators_covered", "evidence_level"]
                
                for field in required_fields:
                    if field not in metadata or not metadata[field] or metadata[field].strip() == "":
                        print(f"Missing or empty field: {field}, filling with default")
                        
                        # Provide intelligent defaults
                        defaults = {
                            "evidence_level": "normative",
                            "country_scope": "Global",
                            "summary": "Humanitarian standard or framework document",
                            "indicators_covered": "Quality and accountability standards"
                        }
                        metadata[field] = defaults.get(field, "Unknown")
                
                # Clean and validate data
                metadata["year"] = str(metadata["year"])
                if len(metadata["short_title"]) > 50:
                    metadata["short_title"] = metadata["short_title"][:47] + "..."
                
                print(f"✓ Successfully extracted metadata for {file_path.name}")
                return metadata
            else:
                print(f"No valid JSON structure found in response")
                return self.get_fallback_metadata(file_path)
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON parsing error for {file_path.name}: {e}")
            print(f"Raw response: {response[:300]}...")
            return self.get_fallback_metadata(file_path)
    
    def get_fallback_metadata(self, file_path: Path) -> Dict[str, str]:
        """Generate intelligent fallback metadata when LLM analysis fails"""
        filename = file_path.stem
        path_str = str(file_path).lower()
        
        # Try to extract year from filename
        year_match = re.search(r'\b(19|20)\d{2}\b', filename)
        year = year_match.group(0) if year_match else "Unknown"
        
        # Try to detect language from filename
        language = "EN"  # default
        if any(lang in filename.lower() for lang in ['fr', 'french', 'français']):
            language = "FR"
        elif any(lang in filename.lower() for lang in ['es', 'spanish', 'español']):
            language = "ES"
        elif any(lang in filename.lower() for lang in ['ar', 'arabic']):
            language = "AR"
        
        # Try to detect publisher from filename or path
        publisher = "Unknown"
        publishers = {
            'sphere': 'Sphere Project',
            'who': 'WHO',
            'unicef': 'UNICEF', 
            'unhcr': 'UNHCR',
            'iasc': 'IASC',
            'chs': 'CHS Alliance',
            'imc': 'IMC'
        }
        
        for key, name in publishers.items():
            if key in filename.lower() or key in path_str:
                publisher = name
                break
        
        # Clean title
        title = filename.replace('_', ' ').replace('-', ' ')
        title = re.sub(r'\b\d{4}\b', '', title)  # Remove year
        title = title.strip().title()
        
        return {
            "title": title,
            "short_title": title[:50] if len(title) <= 50 else title[:47] + "...",
            "publisher": publisher,
            "year": year,
            "language": language,
            "country_scope": "Global",  # Most humanitarian docs are global
            "summary": "Document requires manual review for detailed cataloging",
            "indicators_covered": "To be determined through manual review",
            "evidence_level": "unknown"
        }
    
    def determine_sector(self, file_path: Path) -> str:
        """Determine sector based on file path"""
        path_parts = file_path.parts
        
        for part in path_parts:
            if part in self.sector_mapping:
                return self.sector_mapping[part]
        
        # Try to infer from subdirectories
        for part in path_parts:
            part_lower = part.lower()
            if 'health' in part_lower and 'mhpss' not in part_lower:
                return "Health"
            elif 'mhpss' in part_lower or 'mental' in part_lower:
                return "MHPSS"
            elif 'nutrition' in part_lower:
                return "Nutrition"
            elif 'wash' in part_lower:
                return "WASH"
            elif 'gbv' in part_lower or 'gender' in part_lower:
                return "GBV"
            elif 'protection' in part_lower:
                return "Child Protection"
            elif 'fsl' in part_lower or 'food' in part_lower:
                return "FSL"
                
        return "Cross-Cutting"
    
    def determine_doc_type(self, file_path: Path, title: str) -> str:
        """Determine document type based on path and title"""
        path_str = str(file_path).lower()
        title_lower = title.lower()
        
        if 'standard' in path_str or 'standard' in title_lower:
            return "standard"
        elif 'assessment' in path_str or 'assessment' in title_lower:
            return "assessment_tool"
        elif 'guideline' in path_str or 'guide' in title_lower:
            return "guideline"
        elif 'tool' in path_str or 'tool' in title_lower:
            return "tool"
        elif 'policy' in path_str or 'policy' in title_lower:
            return "policy"
        elif 'example' in path_str or 'example' in title_lower:
            return "example"
        else:
            return "resource"
    
    def generate_doc_id(self, sector: str, doc_type: str, publisher: str, 
                       title: str, year: str, version: str = "v1") -> str:
        """Generate standardized document ID"""
        
        # Clean and abbreviate components
        sector_abbrev = {
            "Health": "HLTH", "MHPSS": "MHPSS", "Nutrition": "NUT", 
            "WASH": "WASH", "GBV": "GBV", "Child Protection": "CP",
            "FSL": "FSL", "Cross-Cutting": "CC", "Mixed": "MX"
        }.get(sector, "GEN")
        
        type_abbrev = {
            "standard": "STD", "assessment_tool": "ASMT", "guideline": "GUID",
            "tool": "TOOL", "policy": "POL", "example": "EX", "resource": "RES"
        }.get(doc_type, "DOC")
        
        # Clean publisher name
        pub_clean = re.sub(r'[^A-Za-z0-9]', '', publisher.upper())[:8]
        if not pub_clean:
            pub_clean = "UNK"
        
        # Clean year
        year_clean = re.findall(r'\d{4}', str(year))
        year_str = year_clean[0] if year_clean else "UNKN"
        
        return f"{sector_abbrev}_{type_abbrev}_{pub_clean}_{year_str}_{version}"
    
    def generate_new_filename(self, doc_id: str, original_path: Path) -> str:
        """Generate new filename based on doc_id"""
        extension = original_path.suffix.lower()
        return f"{doc_id}{extension}"
    
    def process_document(self, file_path: Path, force_reprocess: bool = False) -> Optional[Dict]:
        """Process a single document and return catalog entry"""
        
        # Skip if already processed and file hasn't changed (unless forced)
        relative_path = str(file_path.relative_to(self.kb_path))
        current_checksum = self.get_file_checksum(file_path)
        
        if not force_reprocess and relative_path in self.existing_catalog:
            existing_entry = self.existing_catalog[relative_path]
            if existing_entry.get('checksum_sha256') == current_checksum:
                print(f"Skipping {file_path.name} (unchanged)")
                return existing_entry
            else:
                print(f"Re-processing {file_path.name} (file changed)")
        
        print(f"Processing: {file_path.name}")
        
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text_content = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() == '.docx':
            text_content = self.extract_text_from_docx(file_path)
        else:
            print(f"Unsupported file type: {file_path.suffix}")
            return None
        
        if not text_content:
            print(f"Could not extract text from {file_path}")
            return None
        
        # Analyze with LLM
        llm_metadata = self.analyze_document_with_llm(text_content, file_path)
        
        # Determine additional metadata
        sector = self.determine_sector(file_path)
        doc_type = self.determine_doc_type(file_path, llm_metadata['title'])
        
        # Generate doc_id
        doc_id = self.generate_doc_id(
            sector, doc_type, llm_metadata['publisher'],
            llm_metadata['title'], llm_metadata['year']
        )
        
        # Create catalog entry
        catalog_entry = {
            'doc_id': doc_id,
            'title': llm_metadata['title'],
            'short_title': llm_metadata['short_title'],
            'sector': sector,
            'doc_type': doc_type,
            'doc_source': 'external' if 'External' in str(file_path) else 'internal',
            'publisher': llm_metadata['publisher'],
            'year': llm_metadata['year'],
            'version': 'v1',
            'language': llm_metadata['language'],
            'country_scope': llm_metadata['country_scope'],
            'license': '',  # To be filled manually
            'license_url': '',
            'redistributable': '',
            'url': '',
            'file_name': file_path.name,
            'file_path': relative_path,
            'checksum_sha256': current_checksum,
            'evidence_level': llm_metadata['evidence_level'],
            'last_reviewed': datetime.now().strftime('%m/%d/%y'),
            'next_review_due': (datetime.now() + timedelta(days=365)).strftime('%m/%d/%y'),
            'supersedes_doc_id': '',
            'notes': llm_metadata['summary'],
            'indicators_covered': llm_metadata['indicators_covered'],
            'page_anchors': '',
            'embedding_status': 'pending',
            'embedding_model': '',
            'chunk_count': '',
            'vector_index_id': ''
        }
        
        return catalog_entry
    
    def rename_file(self, original_path: Path, new_filename: str) -> Optional[Path]:
        """Rename file based on doc_id, preserving directory structure"""
        try:
            new_path = original_path.parent / new_filename
            if new_path != original_path and not new_path.exists():
                shutil.move(str(original_path), str(new_path))
                print(f"Renamed: {original_path.name} -> {new_filename}")
                return new_path
            return original_path
        except Exception as e:
            print(f"Error renaming {original_path}: {e}")
            return original_path
    
    def scan_for_file_changes(self) -> Tuple[List[Path], List[str]]:
        """Scan for new and deleted files compared to existing catalog"""
        
        # Find all current PDF and DOCX files
        file_patterns = ['**/*.pdf', '**/*.docx']
        current_files = set()
        
        for pattern in file_patterns:
            files = list(self.kb_path.glob(pattern))
            current_files.update([str(f.relative_to(self.kb_path)) for f in files if not f.name.startswith('.')])
        
        # Get files already in catalog
        cataloged_files = set(self.existing_catalog.keys())
        
        # Find new and deleted files
        new_files = current_files - cataloged_files
        deleted_files = cataloged_files - current_files
        
        new_file_paths = [self.kb_path / f for f in new_files]
        
        return new_file_paths, list(deleted_files)
    
    def clean_deleted_entries(self, deleted_files: List[str]) -> List[Dict]:
        """Remove entries for deleted files from catalog"""
        cleaned_entries = []
        
        for file_path, entry in self.existing_catalog.items():
            if file_path not in deleted_files:
                cleaned_entries.append(entry)
            else:
                print(f"Removing deleted file from catalog: {file_path}")
        
        return cleaned_entries
    
    def catalog_all_documents(self, rename_files: bool = False, incremental: bool = True) -> List[Dict]:
        """Process all documents in the knowledge base"""
        
        print(f"Starting document cataloging in: {self.kb_path}")
        print(f"Using Ollama model: {self.model}")
        print(f"Incremental mode: {incremental}")
        
        if incremental:
            # Scan for changes
            new_files, deleted_files = self.scan_for_file_changes()
            
            print(f"Found {len(new_files)} new documents to process")
            print(f"Found {len(deleted_files)} deleted files to remove from catalog")
            
            # Start with existing entries, minus deleted files
            catalog_entries = self.clean_deleted_entries(deleted_files)
            
            # Process only new files
            files_to_process = new_files
            
            if not new_files and not deleted_files:
                print("No changes detected - catalog is up to date")
                return catalog_entries
                
        else:
            # Full scan mode
            file_patterns = ['**/*.pdf', '**/*.docx']
            all_files = []
            
            for pattern in file_patterns:
                files = list(self.kb_path.glob(pattern))
                all_files.extend([f for f in files if not f.name.startswith('.')])
            
            print(f"Found {len(all_files)} documents to process (full scan)")
            files_to_process = all_files
            catalog_entries = []
        
        # Process files
        for file_path in files_to_process:
            try:
                # Force reprocessing in full scan mode
                entry = self.process_document(file_path, force_reprocess=not incremental)
                if entry:
                    # Rename file if requested
                    if rename_files:
                        new_filename = self.generate_new_filename(entry['doc_id'], file_path)
                        new_path = self.rename_file(file_path, new_filename)
                        if new_path != file_path:
                            # Update entry with new file info
                            entry['file_name'] = new_filename
                            entry['file_path'] = str(new_path.relative_to(self.kb_path))
                    
                    catalog_entries.append(entry)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        return catalog_entries
    
    def save_catalog(self, catalog_entries: List[Dict]) -> None:
        """Save catalog entries to CSV file"""
        
        # Ensure directory exists
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Define field order
        fieldnames = [
            'doc_id', 'title', 'short_title', 'sector', 'doc_type', 'doc_source',
            'publisher', 'year', 'version', 'language', 'country_scope',
            'license', 'license_url', 'redistributable', 'url', 'file_name',
            'file_path', 'checksum_sha256', 'evidence_level', 'last_reviewed',
            'next_review_due', 'supersedes_doc_id', 'notes', 'indicators_covered',
            'page_anchors', 'embedding_status', 'embedding_model', 'chunk_count',
            'vector_index_id'
        ]
        
        try:
            with open(self.catalog_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(catalog_entries)
                
            print(f"\nCatalog saved to: {self.catalog_path}")
            print(f"Total entries: {len(catalog_entries)}")
            
        except Exception as e:
            print(f"Error saving catalog: {e}")

def main():
    """Main execution function"""
    import sys
    
    # Configuration
    KB_PATH = os.path.dirname(os.path.abspath(__file__))  # Current directory by default
    OLLAMA_URL = "http://localhost:11434"
    MODEL = "llama3.2:3b"  # Change to your preferred model
    
    # Parse command line arguments
    rename_files = False
    test_mode = False
    incremental_mode = True
    
    if len(sys.argv) > 1:
        if '--rename' in sys.argv:
            rename_files = True
        if '--test' in sys.argv:
            test_mode = True
        if '--full' in sys.argv:
            incremental_mode = False
        if '--help' in sys.argv or '-h' in sys.argv:
            print("Document Cataloging System")
            print("=" * 50)
            print("Usage: python3 document_cataloger.py [options]")
            print("\nOptions:")
            print("  --rename       Rename files based on generated doc_id")
            print("  --test         Test mode - process only first 3 documents")
            print("  --full         Full scan mode - reprocess all documents")
            print("  --incremental  Incremental mode - only new/changed files (default)")
            print("  --help, -h     Show this help message")
            print("\nModes:")
            print("  Incremental (default): Only processes new files and removes deleted ones")
            print("  Full (--full):         Reprocesses all documents from scratch")
            print("\nExamples:")
            print("  python3 document_cataloger.py                    # Incremental update")
            print("  python3 document_cataloger.py --test             # Test 3 new files")
            print("  python3 document_cataloger.py --full --rename    # Full scan + rename")
            return
    
    print("Document Cataloging System")
    print("=" * 50)
    
    # Check if Ollama is running
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            print("Error: Ollama is not running or not accessible")
            print(f"Please start Ollama and ensure {MODEL} model is available")
            return
    except requests.exceptions.RequestException:
        print("Error: Cannot connect to Ollama")
        print(f"Please start Ollama server at {OLLAMA_URL}")
        return
    
    # Initialize cataloguer
    cataloguer = DocumentCataloguer(
        knowledge_base_path=KB_PATH,
        ollama_url=OLLAMA_URL,
        model=MODEL
    )
    
    # Interactive mode if no arguments provided
    if len(sys.argv) == 1:
        try:
            rename_input = input("Do you want to rename files based on doc_id? (y/n): ")
            rename_files = rename_input.lower().startswith('y')
            
            test_input = input("Run in test mode (process only 3 documents)? (y/n): ")
            test_mode = test_input.lower().startswith('y')
            
            if not test_mode:
                mode_input = input("Run incremental update (only new/changed files) or full scan? (i/f): ")
                incremental_mode = not mode_input.lower().startswith('f')
        except EOFError:
            print("Running in non-interactive mode with default settings...")
            rename_files = False
            test_mode = True
    
    print(f"\nStarting catalog process...")
    print(f"Rename files: {rename_files}")
    print(f"Test mode: {test_mode}")
    if not test_mode:
        print(f"Mode: {'Incremental' if incremental_mode else 'Full scan'}")
    
    # Process documents
    if test_mode:
        # For test mode, find new files if incremental, or first 3 files if full
        if incremental_mode:
            new_files, deleted_files = cataloguer.scan_for_file_changes()
            test_files = new_files[:3]
            print(f"Testing with {len(test_files)} new documents...")
            if deleted_files:
                print(f"Would also remove {len(deleted_files)} deleted files")
        else:
            # Find first 3 documents for testing
            file_patterns = ['**/*.pdf', '**/*.docx']
            test_files = []
            
            for pattern in file_patterns:
                files = list(cataloguer.kb_path.glob(pattern))
                test_files.extend([f for f in files if not f.name.startswith('.')][:3-len(test_files)])
                if len(test_files) >= 3:
                    break
            print(f"Testing with {len(test_files)} documents (full scan mode)...")
        
        catalog_entries = []
        
        # Add existing entries if incremental
        if incremental_mode:
            catalog_entries = cataloguer.clean_deleted_entries(deleted_files if 'deleted_files' in locals() else [])
        
        # Process test files
        for file_path in test_files:
            try:
                entry = cataloguer.process_document(file_path)
                if entry:
                    catalog_entries.append(entry)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
    else:
        catalog_entries = cataloguer.catalog_all_documents(rename_files=rename_files, incremental=incremental_mode)
    
    if catalog_entries:
        # Save catalog
        cataloguer.save_catalog(catalog_entries)
        
        print(f"\n✅ Cataloging complete!")
        print(f"   Processed: {len(catalog_entries)} documents")
        print(f"   Catalog: {cataloguer.catalog_path}")
        
        # Show sample entries
        print(f"\nSample entries:")
        for i, entry in enumerate(catalog_entries[:3]):
            print(f"{i+1}. {entry['doc_id']}: {entry['short_title']}")
    else:
        print("No documents were successfully processed")

if __name__ == "__main__":
    main()