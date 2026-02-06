import pandas as pd
import os
import shutil
import datetime
import argparse
import sys


PROCESSED_FOLDER = 'processed_data'
QUARANTINE_FOLDER = 'quarantine_data'
LOG_FILE = 'pipeline_audit.log'

# 1. LOGGING FUNCTION
def log_message(message):
    """Logs a message with a timestamp to both console and file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    
    
    print(formatted_msg)
    
    # Save to log file
    with open(LOG_FILE, 'a') as f:
        f.write(formatted_msg + "\n")

# 2. VALIDATION LOGIC
def validate_file(file_path):
    try:
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='windows-1252')

        # CHECK 1: Is the file empty?
        if len(df) == 0:
            return False, "File is empty"

        # CHECK 2: Critical Columns Exist?
        required_cols = ['Order ID', 'Sales', 'Profit']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"Missing critical columns: {missing_cols}"

        # CHECK 3: Business Logic (Negative Sales)
        if (pd.to_numeric(df['Sales'], errors='coerce') < 0).any():
             return False, "Contains negative Sales values"
             
        return True, "Passed all checks"

    except Exception as e:
        return False, f"Critical Read Error: {str(e)}"

# 3. MAIN PIPELINE LOGIC
def process_batch(input_folder):
    log_message(f"--- INITIALIZING PIPELINE FOR: {input_folder} ---")
    
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(QUARANTINE_FOLDER, exist_ok=True)

    try:
        files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    except FileNotFoundError:
        log_message(f"CRITICAL ERROR: Input folder '{input_folder}' not found.")
        return

    if not files:
        log_message("No CSV files found in input directory.")
        return

    stats = {'processed': 0, 'quarantined': 0}

    for filename in files:
        source_path = os.path.join(input_folder, filename)
        log_message(f"Auditing file: {filename}...")
        
        is_valid, reason = validate_file(source_path)
        
        if is_valid:
            destination = os.path.join(PROCESSED_FOLDER, filename)
            if os.path.exists(destination):
                os.remove(destination)
            shutil.move(source_path, destination)
            log_message(f"SUCCESS: File valid. Moved to {PROCESSED_FOLDER}")
            stats['processed'] += 1
        else:
            destination = os.path.join(QUARANTINE_FOLDER, filename)
            if os.path.exists(destination):
                os.remove(destination)
            shutil.move(source_path, destination)
            log_message(f"FAILURE: {reason}. Moved to {QUARANTINE_FOLDER}")
            stats['quarantined'] += 1

    log_message("--- BATCH COMPLETE ---")
    log_message(f"Summary: {stats['processed']} Valid | {stats['quarantined']} Rejected")

# 4. CLI ENTRY POINT
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Data Ingestion Pipeline")
    parser.add_argument('--input', type=str, required=True, help="Path to the input folder containing CSVs")
    
    args = parser.parse_args()
    

    process_batch(args.input)

