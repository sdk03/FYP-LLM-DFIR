# Dataset Documentation

This directory contains the datasets and utility scripts used to simulate and prepare forensic artifacts for Component A of the project *"Leveraging Large Language Models for Automated Digital Forensic Analysis."*

---

## 1. Overview

The dataset is constructed to emulate SMS data as typically extracted from Android mobile devices during digital forensic investigations. It is used primarily for evaluating the performance of an Autopsy-integrated plugin for entity-based message categorization via Large Language Models (LLMs).

---

## 2. Data Sources

SMS messages were aggregated from three publicly available corpora:

- **UCI SMS Spam Collection** 
- **NUS Singapore SMS Corpus**
- **Indian SMS Corpus**

These sources were selected to introduce linguistic and regional diversity, reflecting realistic forensic challenges.

---

## 3. Dataset Construction Process

The construction pipeline consists of the following stages:

| Step | Description |
|------|-------------|
| **1. Sampling** | A representative subset of messages was randomly selected from each dataset using the script `samplePicker.py`. |
| **2. SQL Conversion** | Sampled messages were converted into SQL `INSERT` queries using `sqlGen.py`. |
| **3. SQLite Injection** | The resulting queries were executed into a SQLite database named `mmssms.db`, which mimics the schema used by Android SMS storage (compatible with Autopsy). |

The resulting database simulates a forensic SMS artifact and can be directly ingested into digital forensic tools.

---

## 4. Ground Truth Annotations

A subset of 100 messages from the emulated database was manually annotated to serve as ground truth for evaluation. Each message was labeled with one or more forensic-relevant entity types (e.g., `Date`, `Currency`, `Name`, `Phone Number`, etc.).

These labels are stored in `labeled_sms.csv`, which supports evaluation of classification metrics including Precision, Recall, F1 Score, and MCC.

---

## 5. Data Processing

No additional preprocessing (e.g., text normalization or cleaning) was performed.

---

## 6. Directory Structure

```plaintext
dataset/
├── mmssms.db              # SQLite database simulating Android SMS storage
├── scripts/
│   ├── samplePicker.py    # Script to sample records from the source corpora
│   └── sqlGen.py          # Script to convert sampled messages into SQL insert
└── README.md              # Dataset documentation (this file)
