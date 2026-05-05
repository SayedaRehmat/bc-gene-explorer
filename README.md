# 🧬 BC Gene Explorer

A breast cancer gene expression visualization and biomarker interpretation tool designed for rapid exploration of tumor vs normal expression patterns, pathway context, and clinical relevance.

---

## Overview

BC Gene Explorer is a lightweight computational biology dashboard that enables interactive exploration of breast cancer biomarkers using gene expression data.

It is designed for:

- Rapid biomarker screening  
- Tumor vs normal expression comparison  
- Pathway-level interpretation  
- Clinical annotation of gene signatures  
- Educational and research prototyping  

The project simulates a real translational bioinformatics workflow using clean, interpretable visual analytics.

---

## Key Features

- Interactive gene selection panel  
- Tumor vs Normal expression visualization  
- log2 fold-change and statistical summary  
- Biological function annotation  
- Pathway-level interpretation  
- Clinical biomarker insights  
- Automated PDF report generation  
- Clean biomedical dashboard UI  

---

## Example Use Cases

This tool helps in exploring:

- HER2 amplification (ERBB2) in breast cancer  
- Hormone receptor status (ESR1, PGR)  
- Proliferation markers (MKI67, MYC)  
- Tumor suppressor disruption (TP53, PTEN)  
- Basal vs luminal subtype signals  

---

## Example Genes Included

- BRCA1  
- BRCA2  
- TP53  
- ERBB2  
- ESR1  
- PGR  
- MKI67  
- MYC  
- PTEN  
- EGFR  
- PIK3CA  
- GATA3  
- KRT5  
- KRT14  

---

## Project Structure

bc-gene-explorer/

├── app.py  
├── report.py  
├── requirements.txt  
├── .gitignore  
├── README.md  
│  
├── data/  
│   ├── mock_expression.csv  
│   └── gene_info.json  
│  
├── assets/  
│   └── screenshots/  
│       ├── home_dashboard.png  
│       └── gene_view_erbb2.png  
│  
└── reports/  
    └── sample_gene_report.pdf  

---

## Installation & Usage

### Clone Repository

git clone https://github.com/your-username/bc-gene-explorer.git  
cd bc-gene-explorer  

---

### Install Dependencies

pip install -r requirements.txt  

---

### Run Application

streamlit run app.py  

---

### Generate PDF Report

python report.py  

This creates:

reports/sample_gene_report.pdf  

---

## Output

The system generates:

- Gene-level expression summaries  
- Tumor vs normal comparison charts  
- Biological function annotations  
- Pathway-level interpretation  
- Clinical biomarker insights  
- Downloadable PDF reports  

---

## Scientific Interpretation Layer

Each gene is annotated with:

- Molecular function  
- Pathway involvement  
- Biomarker classification  
- Clinical relevance  

---

## UI Design Philosophy

- Minimal and clean layout  
- Card-based visualization  
- Biomedical color structure  
- Scientific dashboard feel  
- Focus on interpretability  

---

## Future Enhancements

- Integration with TCGA / GEO datasets  
- Multi-gene signature analysis  
- Survival analysis module  
- Pathway enrichment visualization  
- ML-based subtype classification  
- SHAP explainability layer  

---

## Disclaimer

This project is a research prototype built for educational and demonstration purposes. It does not use real clinical patient data.

---

## Author

Sayeda Rehmat  
Bioinformatics | Computational Biology | Translational AI  

---

## Purpose

This project demonstrates:

- Computational biology workflow design  
- Biomarker interpretation logic  
- Bioinformatics visualization engineering  
- Prototype-level translational AI system design  
