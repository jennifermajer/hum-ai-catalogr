# 🧠 hum-ai-catalogr

## AI-Ready Knowledge Base Cataloging System

hum-ai-catalogr is an intelligent document cataloging system that transforms unstructured humanitarian document collections into structured, AI-ready knowledge bases. It leverages LLM-powered metadata extraction and standardized taxonomies to support fine-tuning, retrieval-augmented generation (RAG), and grounded AI applications.

Originally developed as part of the **AI-Assisted Needs Assessment Assistant (AINAA)** project under the ELRHA / UKHIH “AI Solutions for Humanitarian Challenges” initiative, this tool addresses a critical bottleneck in AI development: curating structured, high-quality metadata for diverse and fragmented humanitarian knowledge sources.

## Why This Matters

Building effective AI systems requires high-quality, structured data. This system is:

- **🎯 Practical** — Solves a common bottleneck: structured, high-quality metadata for large document sets
- **🧠 AI-integrated** — Uses local LLMs (Ollama) for intelligent tagging, summarization, and classification  
- **🔄 Reproducible** — CLI-based Python workflow with optional automation hooks
- **🔧 Flexible** — Supports local models (LLaMA3/Ollama), multiple formats (PDF, DOCX), user-defined schemas
- **🔒 Security-focused** — Designed for sensitive documents with local-only processing, no cloud API dependencies

## Use Cases

This system enables:

- **🤖 LLM Fine-tuning** — Curating training corpora from domain-specific documents
- **🔍 RAG Pipelines** — Building vectorized knowledge stores with traceable metadata  
- **📚 Knowledge Base Creation** — Structured repositories for humanitarian aid, climate response, health guidance, etc.
- **📊 Document Analytics** — Large-scale analysis of document collections with consistent tagging

## Project Background

Developed for humanitarian AI applications where document quality and traceability are critical. The system processes diverse document types (standards, guidelines, assessments, policies) into a unified catalog suitable for:

- Vector database ingestion
- LLM training data preparation  
- Automated content analysis
- Knowledge graph construction

## Core Features

### 🤖 Intelligent Metadata Extraction
- **Local LLM analysis** using Ollama for privacy and security
- **Multi-language support** (English, French, Spanish, Arabic)
- **Domain-aware classification** for humanitarian, health, and policy documents
- **Automated summarization** and key indicator identification

### 📋 Standardized Taxonomies  
- **Structured document IDs**: `HLTH_STD_WHO_2023_v1` (Health Standard by WHO, 2023)
- **Sector classification**: Health, WASH, Nutrition, MHPSS, GBV, Child Protection, etc.
- **Document typing**: Standards, assessments, guidelines, policies, examples
- **Evidence grading**: Normative, evidence-based, operational, example

### 🔄 Incremental Processing
- **Smart updates**: Only processes new or changed files
- **Change detection**: Uses checksums to identify modifications  
- **Deleted file cleanup**: Automatically removes obsolete entries
- **Batch processing**: Handles large document collections efficiently

### 📁 Multi-format Support
- **PDF text extraction** with robust error handling
- **DOCX processing** including structured content
- **Extensible architecture** for additional formats
- **File integrity verification** via SHA256 checksums

### 🎛️ Flexible Configuration
- **Secure local processing**: Ollama LLM ensures sensitive documents never leave your infrastructure
- **Customizable schemas**: Adapt fields for your domain
- **CLI and programmatic APIs**: Integrate into existing workflows
- **Optional file renaming**: Align filenames with generated IDs

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Document      │    │   LLM Analysis   │    │   Structured    │
│   Collection    │───▶│   & Extraction   │───▶│    Catalog      │
│  (PDF, DOCX)    │    │ (Local Ollama)   │    │    (CSV)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  File System    │    │  Metadata Schema │    │  AI Pipeline    │
│   Monitoring    │    │  & Taxonomies    │    │   Integration   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Data Flow

1. **Discovery**: Scans directory structure for PDF/DOCX files
2. **Change Detection**: Compares against existing catalog using checksums  
3. **Content Extraction**: Extracts text from documents with format-specific parsers
4. **LLM Analysis**: Sends text to LLM for metadata extraction and classification
5. **Schema Mapping**: Converts LLM output to standardized catalog fields
6. **Catalog Update**: Writes results to CSV with proper versioning and integrity checks

### Output Schema

Generated catalogs include 29+ fields optimized for AI workflows:

| Field Category | Examples | Purpose |
|---------------|-----------|---------|
| **Identity** | `doc_id`, `title`, `short_title` | Unique identification and referencing |
| **Classification** | `sector`, `doc_type`, `evidence_level` | Taxonomic organization |
| **Provenance** | `publisher`, `year`, `country_scope` | Source tracking and attribution |  
| **Content** | `summary`, `indicators_covered` | Semantic understanding |
| **Technical** | `checksum`, `file_path`, `language` | Processing and integration |
| **AI-Ready** | `embedding_status`, `vector_index_id` | Pipeline integration markers |

## Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) for secure local LLM processing
- [Visual Studio Code](https://code.visualstudio.com) (recommended development environment)
- Git for version control

### 1. Clone and Setup

```bash
git clone <repository-url>
cd ai-knowledge-cataloger

# Install Python dependencies
pip install -r requirements.txt

# Or use the setup script
chmod +x setup_cataloger.sh
./setup_cataloger.sh
```

### 2. Setup Local LLM (Ollama)

**Secure Local Processing - No Cloud Dependencies**
```bash
# Install Ollama for local LLM processing
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required model (runs entirely on your hardware)
ollama pull llama3.2:3b

# Start Ollama server (localhost only)
ollama serve
```

**Why Local Processing?**
- **🔒 Complete Privacy**: Documents never leave your infrastructure
- **🚫 No API Costs**: No per-request charges or rate limits  
- **🌐 Offline Capable**: Works without internet connectivity
- **🔐 Sensitive Data Safe**: Ideal for confidential/proprietary documents

### 3. Test Installation

```bash
# Test system components
python3 test_cataloger.py

# Explore example outputs (no documents needed)
head examples/kb_catalog_template.csv

# Test with your own documents
python3 document_cataloger.py --test
```

## Getting Started

### Explore Examples First (Recommended)

Before processing your own documents, explore the included examples:

```bash
# View sample catalog output with realistic humanitarian documents
head examples/kb_catalog_template.csv

# Understand document classification system  
cat examples/document_id_examples.md

# See automated analysis capabilities
cat examples/sample_analysis_report.md
```

These examples show:
- **Complete catalog structure** with all 29 fields populated
- **Document ID generation** for different sectors and types
- **Multi-language processing** capabilities  
- **Analysis and reporting** features for AI pipeline integration

## Usage

### Command Line Interface

```bash
# Quick help
python3 document_cataloger.py --help

# Incremental processing (recommended)  
python3 document_cataloger.py              # Process new/changed files only

# Full reprocessing
python3 document_cataloger.py --full       # Reprocess all documents

# Test modes
python3 document_cataloger.py --test       # Process 3 files for testing

# Advanced options
python3 document_cataloger.py --full --rename  # Full scan + file renaming
```

### Workflow

1. **Place documents** in your target directory structure
2. **Run cataloger**: `python3 document_cataloger.py`
3. **Review output**: Check generated `kb_catalog.csv`
4. **Iterate**: Add more documents and run incrementally

The system will:
- 🔍 Scan directory structure for PDF/DOCX files
- 🤖 Extract metadata using LLM analysis  
- 📊 Generate structured catalog with 29+ fields
- ⚡ Skip unchanged files for efficiency

## Configuration

### Basic Configuration

Edit configuration in `document_cataloger.py`:

```python
# Path Configuration
KB_PATH = "/path/to/your/documents"           # Your document directory
CATALOG_FILE = "catalog/kb_catalog.csv"       # Output catalog location

# Local LLM Configuration  
OLLAMA_URL = "http://localhost:11434"         # Local Ollama server URL
MODEL = "llama3.2:3b"                         # Local model name

# Processing Options
DEFAULT_LANGUAGE = "EN"                       # Fallback language
DEFAULT_COUNTRY_SCOPE = "Global"              # Default geographic scope
```

### Custom Taxonomies

Adapt sector and document type mappings for your domain:

```python
# Example: Climate/Environmental Focus
self.sector_mapping = {
    "climate_adaptation": "Climate Adaptation",
    "renewable_energy": "Renewable Energy", 
    "biodiversity": "Biodiversity",
    "carbon_markets": "Carbon Markets"
}

# Example: Healthcare Focus  
self.doc_type_mapping = {
    "clinical_guidelines": "clinical_guideline",
    "research_protocols": "research_protocol",
    "patient_education": "patient_resource"
}
```

### Integration Examples

**RAG Pipeline Integration**
```python
# Load catalog for vector database ingestion
import pandas as pd
catalog = pd.read_csv('kb_catalog.csv')

# Filter for high-quality documents
quality_docs = catalog[
    (catalog['evidence_level'] == 'normative') & 
    (catalog['language'] == 'EN')
]

# Use file_path for document loading
for _, doc in quality_docs.iterrows():
    content = load_document(doc['file_path'])
    embeddings = embed_text(doc['summary'])
    vector_db.insert(doc['doc_id'], content, embeddings, doc.to_dict())
```

**Training Data Curation**
```python  
# Select documents by criteria
training_docs = catalog[
    (catalog['sector'].isin(['Health', 'WASH'])) &
    (catalog['year'] >= 2020) &
    (catalog['evidence_level'] != 'example')
]

# Create training corpus with metadata
training_data = []
for _, doc in training_docs.iterrows():
    text = extract_text(doc['file_path'])
    metadata = {
        'source': doc['publisher'],
        'domain': doc['sector'], 
        'quality': doc['evidence_level']
    }
    training_data.append({'text': text, 'metadata': metadata})
```

## Generated Catalog Fields

The system populates these key fields in `kb_catalog.csv`:

- **doc_id**: Standardized identifier (e.g., `HLTH_STD_WHO_2023_v1`)
- **title**: Full document title extracted from content
- **short_title**: Abbreviated title (max 50 characters)
- **sector**: Health, WASH, Nutrition, MHPSS, GBV, etc.
- **doc_type**: standard, assessment_tool, guideline, policy, etc.
- **publisher**: Publishing organization
- **year**: Publication year
- **language**: Language code (EN, FR, ES, AR, etc.)
- **country_scope**: Geographic scope (Global, Regional, or specific country)
- **notes**: AI-generated summary of document content
- **indicators_covered**: Key metrics and standards covered
- **evidence_level**: Assessment of evidence quality
- **checksum_sha256**: File integrity checksum

## Document ID Convention

The system generates IDs using this pattern:
`{SECTOR}_{TYPE}_{PUBLISHER}_{YEAR}_{VERSION}`

**Sector Abbreviations:**
- HLTH: Health
- MHPSS: Mental Health & Psychosocial Support  
- NUT: Nutrition
- WASH: Water, Sanitation & Hygiene
- GBV: Gender-Based Violence
- CP: Child Protection
- FSL: Food Security & Livelihoods
- CC: Cross-Cutting
- MX: Mixed/Multi-sector

**Type Abbreviations:**
- STD: Standard
- ASMT: Assessment Tool
- GUID: Guideline
- TOOL: Tool
- POL: Policy
- EX: Example
- RES: Resource

## File Organization

The system preserves your existing directory structure and can optionally rename files:

**Before:**
```
04_Sector_Assessment_Guidelines_Tools/Health/WHO Mortality Survey Guide.pdf
```

**After (if rename enabled):**
```
04_Sector_Assessment_Guidelines_Tools/Health/HLTH_GUID_WHO_2023_v1.pdf
```

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check the model is available: `ollama list`
- Verify the URL in configuration matches your Ollama setup

### PDF/DOCX Extraction Issues
- Some encrypted or complex formatted files may not extract text properly
- The system will use fallback metadata for failed extractions
- Check file permissions and ensure files aren't corrupted

### Performance
- Processing large collections can take time (1-2 minutes per document)
- The system skips already processed files on subsequent runs
- Consider processing in batches for very large collections

## Manual Review

After automated cataloging, review the generated entries for:
- Accuracy of extracted metadata
- License and redistribution information
- URL links to original sources
- Page anchor information for key sections

The system marks fields it couldn't determine automatically for manual completion.


## Troubleshooting

### Common Issues

**LLM Connection Problems**
```bash
# Check Ollama status
ollama list                    # Show available models
curl http://localhost:11434    # Test connection

# Restart if needed
pkill ollama && ollama serve
```

**Memory/Performance Issues**
```bash
# Use smaller model for large batches
MODEL = "llama3.2:1b"         # Faster, less accurate

# Process in smaller batches  
python3 document_cataloger.py --test  # Test with 3 files
```

**Text Extraction Problems**
- **Encrypted PDFs**: System will skip and log errors
- **Complex formatting**: May result in garbled text, triggering fallback metadata
- **Large files**: Consider breaking into smaller sections

**Catalog Inconsistencies**
```bash
# Force full reprocessing
python3 document_cataloger.py --full

# Reset catalog completely  
rm kb_catalog.csv && python3 document_cataloger.py --full
```

## Contributing

We welcome contributions! This project benefits from:

### Immediate Needs
- **Additional format support** (PowerPoint, Excel, web pages)
- **Multi-language prompts** for better non-English extraction
- **Schema extensions** for specific domains (legal, scientific, etc.)

### Development Setup

**Visual Studio Code Environment (Recommended)**

This project was developed and tested using Visual Studio Code with specific extensions and settings:

```bash
git clone <repository-url>
cd ai-knowledge-cataloger

# Open in VS Code
code .

# Install recommended VS Code extensions:
# - Python (Microsoft)
# - Python Docstring Generator
# - Pylance (Microsoft) 
# - Black Formatter
# - Markdown All in One
```

**Development Dependencies**
```bash
# Development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Code formatting (as used in development)
black document_cataloger.py
```

**VS Code Settings**
The project includes `.vscode/settings.json` with optimal configurations for:
- Python path detection
- Linting with pylint
- Formatting with Black
- Markdown linting

### Contribution Guidelines
1. **Fork** and create feature branch
2. **Add tests** for new functionality
3. **Update documentation** for API changes
4. **Submit PR** with clear description and examples

## Roadmap

- **v2.0**: OpenAI integration, web interface
- **v2.1**: Multi-modal support (images, tables, charts)
- **v2.2**: Real-time monitoring and auto-cataloging  
- **v3.0**: Knowledge graph generation and entity linking

## License & Citation

### License
This project is released under the **MIT License**.

### Citation
If you use this system in research or production, please cite:

```bibtex
@software{ai_knowledge_cataloger_2025,
  title = {AI-Ready Knowledge Base Cataloging System},
  author = {AINAA Development Team},
  year = {2025},
  url = {https://github.com/your-org/ai-knowledge-cataloger},
  note = {Developed for ELRHA/UKHIH AI Solutions for Humanitarian Challenges initiative}
}
```

### Acknowledgments
- **ELRHA/UKHIH** for funding the AI Solutions for Humanitarian Challenges initiative
- **Ollama team** for local LLM infrastructure
- **Humanitarian community** for document standards and taxonomies that inform our classification systems
- **Claude Code (Anthropic)** for accelerating development and saving days of manual coding work 🎉

---

## Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Community**: Join discussions in GitHub Discussions
- **Contact**: For collaboration opportunities on humanitarian AI projects

**Built with ❤️ for the humanitarian community and AI researchers worldwide.**