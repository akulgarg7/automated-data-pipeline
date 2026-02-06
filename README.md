# Automated Data Ingestion & Integrity Pipeline

A Python-based Command Line Interface (CLI) tool designed to automate the validation, sorting, and quarantining of large-scale CSV batches.

## 📌 Project Overview
In production data environments, "dirty" or corrupt data can break downstream analysis pipelines. This tool acts as a **Gatekeeper**. It scans a directory of incoming CSV files, validates them against strict business rules, and automatically sorts them into:
* **Processed:** Clean files ready for the database/analysis.
* **Quarantine:** Corrupt or schema-non-compliant files that need manual review.

This project demonstrates **Systems Automation**, **File I/O Management**, and **Robust Error Handling**.

## 🚀 Key Features
* **CLI Support:** Built with `argparse` to run from the terminal with custom input paths, making it easy to schedule via cron jobs or shell scripts.
* **Quarantine Architecture:** Automatically moves corrupt files to a safe isolation folder to prevent system pollution.
* **Batch Processing:** Iterates through high volumes of files without manual intervention.
* **Audit Logging:** Generates a timestamped `pipeline_audit.log` file for every action taken (Success/Failure), providing a full audit trail.
* **Encoding Fallback:** Automatically handles different file encodings (UTF-8 vs Windows-1252) to prevent crashes on legacy files.

## 📂 Project Structure
The script manages the following directory structure automatically:

```text
Automated_Data_Pipeline/
│
├── ingestor.py              # Main CLI Application
├── pipeline_audit.log       # System Log (Auto-generated)
│
├── incoming_data/           # Place raw CSVs here
│   ├── new_sales_data.csv
│   └── ...
│
├── processed_data/          # Clean files are moved here by the script
│
└── quarantine_data/         # Bad files are moved here by the script
