# Document Cataloger - Quick Start Guide


## 🚀 Two Ways to Get Started

### Option A: Try the Examples (No Documents Needed)

**Perfect for exploring the system capabilities without your own documents**

```bash
# View example catalog output
head -5 examples/kb_catalog_template.csv

# See example document classifications  
cat examples/document_id_examples.md

# Review sample analysis report
cat examples/sample_analysis_report.md

# Test system components (uses sample data)
python3 test_cataloger.py
```

### Option B: Catalog Your Own Documents

**For processing your actual document collection**

#### 1. Setup Your Documents
```bash
# Place your PDF/DOCX files in the knowledge base directory
# Example structure:
# documents/
# ├── standards/
# │   ├── health_standard.pdf
# │   └── wash_guidelines.docx
# └── assessments/
#     └── assessment_tool.pdf
```

#### 2. Run the Cataloger
```bash
# Show all available options
./run_cataloger.sh help

# Test with 3 of your documents first
./run_cataloger.sh --test

# Check what will be processed (shows new/changed files)
python3 test_incremental.py

# Process all your new documents (incremental mode)
./run_cataloger.sh                          # Default - only new/changed files

# Full processing of all documents
./run_cataloger.sh --full                   # Reprocess everything

# Full processing + rename files to match doc IDs  
./run_cataloger.sh --full --rename
```

#### 3. Review Results
```bash
# Check your generated catalog
head -10 00_Governance/kb_catalog.csv

# Generate analysis report for your collection
python3 analyze_catalog.py 00_Governance/kb_catalog.csv
```

### 🆕 **Incremental Features**

- **Smart Updates**: Only processes new or changed files
- **Deleted File Cleanup**: Automatically removes entries for deleted files  
- **Change Detection**: Shows what will be updated before processing
- **Faster Processing**: Skip unchanged files, much faster for large collections

## 📁 What You Have

- **`document_cataloger.py`** - Main cataloging system
- **`test_cataloger.py`** - Component testing script  
- **`run_cataloger.sh`** - Wrapper script that uses the correct Python
- **`requirements.txt`** - Dependencies
- **`examples/`** - Template files and demonstrations
- **`CATALOGER_README.md`** - Full documentation

## 🔧 Development Environment

**This project was developed using:**

### Visual Studio Code Setup
```bash
# Recommended VS Code extensions for full compatibility:
# - Python (ms-python.python)
# - Pylance (ms-python.vscode-pylance)  
# - Python Docstring Generator (njpwerner.autodocstring)
# - Black Formatter (ms-python.black-formatter)
# - Markdown All in One (yzhang.markdown-all-in-one)

# Open project in VS Code
code .
```

### System Environment Used
- **OS**: macOS (Darwin 23.6.0)  
- **Python**: 3.12.4+ (Anaconda distribution)
- **Terminal**: Bash shell with conda environment
- **LLM**: Ollama with llama3.2:3b model locally installed

### Python Environment
```bash
# The system was developed with both system Python and Anaconda
# Anaconda (preferred): /opt/anaconda3/bin/python3
# System Python: /usr/local/bin/python3  

# Check your Python version matches:
python3 --version  # Should be 3.8+ 

# Verify packages install correctly:
pip3 install -r requirements.txt
```

## 🎯 Next Steps

### For Example Exploration:
1. **Review examples**: `cat examples/kb_catalog_template.csv`
2. **Understand classifications**: `cat examples/document_id_examples.md`
3. **Study analysis format**: `cat examples/sample_analysis_report.md`

### For Your Own Documents:
1. **Start Ollama** (if not running): `ollama serve`
2. **Place your documents** in the directory structure
3. **Test with sample**: `./run_cataloger.sh --test` 
4. **Run full cataloging**: `./run_cataloger.sh` (incremental mode)
5. **Review results**: Check generated `kb_catalog.csv`

## 🔧 System Status

✅ Python packages installed correctly  
✅ PDF text extraction working  
✅ Document ID generation working  
✅ Sector detection working  
✅ Ollama connection available  
✅ All components tested successfully  

The system is ready to catalog your knowledge base!