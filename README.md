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
```
## 🛠️ Validation Logic
The script runs the following checks on every CSV file:
1.  **Empty File Check:** Rejects files with zero rows.
2.  **Schema Validation:** Ensures critical columns (`Order ID`, `Sales`, `Profit`) exist.
3.  **Business Logic:** Flags rows where `Sales < 0` (Negative revenue is impossible in this context).

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/akulgarg7/automated-data-pipeline.git](https://github.com/akulgarg7/automated-data-pipeline.git)
    cd automated-data-pipeline
    ```

2.  **Install Dependencies**
    The only external library required is `pandas` (for efficient file parsing). All others (`os`, `shutil`, `argparse`, `sys`, `datetime`) are built-in Python libraries.
    ```bash
    pip install pandas
    ```

## 💻 Usage

1.  Place your raw CSV files inside the `incoming_data` folder.
2.  Run the script from your terminal:

    ```bash
    python ingestor.py --input incoming_data
    ```

3.  **Verify Results:**
    * Valid files will move to `processed_data/`.
    * Invalid files will move to `quarantine_data/`.
    * Check `pipeline_audit.log` for details.

## 📝 Example Output (Log)
```text
[2026-02-06 20:28:35] --- INITIALIZING PIPELINE FOR: incoming_data ---
[2026-02-06 20:28:35] Auditing file: corrupt_data.csv...
[2026-02-06 20:28:36] FAILURE: Missing critical columns: ['Sales']. Moved to quarantine_data
[2026-02-06 20:28:36] Auditing file: Superstore.csv...
[2026-02-06 20:28:36] SUCCESS: File valid. Moved to processed_data
[2026-02-06 20:28:36] --- BATCH COMPLETE ---
