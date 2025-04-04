# Dataset Documentation

This directory contains the finalized dataset used in **Component A** of the project:  
**"Leveraging Large Language Models for Automated Digital Forensic Analysis."**

---

## Overview

The dataset has been fully processed and is provided in the form of a SQLite database file (`mmssms.db`). This database emulates the structure of an Android SMS storage artifact and is intended for direct ingestion into digital forensic tools such as **Autopsy**.

No further preprocessing or transformation is required.

---

## Contents

| File              | Description |
|------------------|-------------|
| `mmssms.db`       | A SQLite database containing SMS messages formatted in the Android `mmssms.db` schema. Compatible with Autopsy for forensic analysis and plugin evaluation. |
| `labeled_sms.csv` | Ground truth annotations for 100 selected SMS messages, labeled across 16 forensic-relevant entity categories for evaluation purposes. |

---

## Usage

To use the dataset:

1. Import `mmssms.db` as part of your digital forensic case in Autopsy.
2. Use the provided Autopsy plugin to categorize messages.

---

## Notes

- The dataset is fully anonymized and compiled from public sources for academic use.
- No raw or intermediate files are included, as the processed SQLite file is ready for immediate use.

---

**Return to main project repository:** [../README.md](../README.md)
