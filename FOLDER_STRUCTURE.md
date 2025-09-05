# Knowledge Base Folder Structure

This document explains the organizational structure used for the humanitarian knowledge base that this cataloging system processes.

## Directory Structure Overview

```
Knowledge Base/
├── 00_Governance/                          # System governance and catalogs
│   ├── kb_catalog.csv                     # Main catalog output
│   └── kb_catalog_backup.csv             # Backup copies
├── 01_Cross_Cutting_Standards/            # Multi-sector standards
├── 02_Sector_Standards_Policies/          # Sector-specific standards
│   ├── Health/
│   │   ├── Internal_Standards/           # Organization-specific standards
│   │   └── External_Standards/           # Public standards (WHO, etc.)
│   ├── WASH/
│   ├── Nutrition/
│   ├── MHPSS/
│   ├── GBV/
│   └── Child_Protection/
├── 03_Cross_Cutting_Assessment_Guidelines_Tools/  # Multi-sector assessments
│   ├── Internal/                         # Organization tools
│   └── External/                         # Public assessment frameworks
├── 04_Sector_Assessment_Guidelines_Tools/  # Sector-specific assessments
│   ├── Health/
│   ├── WASH/
│   ├── Nutrition/
│   ├── MHPSS/
│   └── GBV/
├── 05_Gold_Standard_Examples/              # Reference examples
│   ├── 01_Multi_Sector/
│   │   ├── Internal_Examples/            # Organization case studies
│   │   └── External_Examples/            # Public examples
│   └── 02_Sector_Specific/
└── 06_Modeling_Artifacts/                  # AI/ML outputs
```

## Design Principles

### 1. Hierarchical Organization
- **00-06 Prefix System**: Ensures consistent ordering and processing sequence
- **Sector-Specific Grouping**: Documents grouped by humanitarian sector (Health, WASH, etc.)
- **Document Type Classification**: Standards, assessments, guidelines, examples

### 2. Internal vs External Distinction
- **Internal**: Organization-specific documents, proprietary content, sensitive materials
- **External**: Publicly available standards, frameworks published by UN agencies, NGOs, etc.
- **Purpose**: Enables different handling for licensing, security, and distribution

### 3. Document Type Categories

#### Standards & Policies (01, 02)
- **Cross-Cutting**: Multi-sector standards (Sphere, CHS, HAP)  
- **Sector Standards**: Technical standards for specific sectors
- **Internal Policies**: Organization-specific guidelines and procedures

#### Assessment Tools (03, 04)  
- **Guidelines**: How to conduct assessments
- **Tools**: Questionnaires, checklists, templates
- **Frameworks**: Assessment methodologies and approaches

#### Examples & References (05)
- **Gold Standards**: Best practice examples and case studies
- **Implementation Examples**: Real-world applications and lessons learned
- **Templates**: Reusable formats and structures

## Cataloging Implications

### Automated Classification
The folder structure enables automatic:
- **Sector Detection**: Based on folder path (Health, WASH, etc.)
- **Document Type**: Based on folder category (Standards, Assessment, etc.)
- **Source Classification**: Internal vs External handling
- **Processing Priority**: Standards processed before examples

### Security & Licensing
- **Internal Documents**: Not included in public repositories
- **External Documents**: Handled according to original licensing  
- **Sensitive Content**: Excluded from git while preserving structure
- **Metadata Only**: Catalogs contain references, not content

### AI Pipeline Integration
- **Training Data**: Standards and guidelines for high-quality training
- **RAG Content**: Assessments and tools for practical queries  
- **Example Learning**: Gold standards for few-shot learning
- **Quality Filtering**: Internal/External distinction for content curation

## Usage for Replication

### For Other Organizations
This structure can be adapted by:

1. **Replacing Sectors**: Modify 02_Sector_* and 04_Sector_* for your domain
2. **Internal Content**: Populate Internal_* folders with your organization's documents
3. **External Sources**: Add relevant public standards and frameworks  
4. **Custom Categories**: Add numbered folders (07_, 08_) for domain-specific needs

### For Different Domains

#### Climate/Environmental
```
02_Sector_Standards_Policies/
├── Climate_Adaptation/
├── Renewable_Energy/
├── Biodiversity/
└── Carbon_Markets/
```

#### Healthcare Systems  
```
02_Sector_Standards_Policies/
├── Clinical_Care/
├── Public_Health/
├── Health_Systems/
└── Medical_Research/
```

#### Legal/Governance
```
02_Sector_Standards_Policies/
├── Policy_Framework/
├── Legal_Standards/
├── Governance/
└── Compliance/
```

This structure balances organization, security, and AI processing requirements while remaining adaptable to different domains and use cases.