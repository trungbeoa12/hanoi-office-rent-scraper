"""
CSV file management utilities
"""
import csv
import os
from pathlib import Path
from ..config import OUTPUT_DIR


class CSVManager:
    """Manages CSV file operations"""
    
    def __init__(self, filename):
        self.filename = filename
        self.filepath = OUTPUT_DIR / filename
    
    def write_header_if_needed(self, fieldnames):
        """Write CSV header if file doesn't exist or is empty"""
        if not self.filepath.exists() or self.filepath.stat().st_size == 0:
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
    
    def append_row(self, data):
        """Append a row to CSV file"""
        file_exists = self.filepath.exists()
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            if file_exists:
                # Get existing fieldnames
                with open(self.filepath, "r", encoding="utf-8") as read_f:
                    reader = csv.DictReader(read_f)
                    fieldnames = reader.fieldnames
            else:
                fieldnames = list(data.keys())
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    
    def get_row_count(self):
        """Get number of rows in CSV file"""
        if not self.filepath.exists():
            return 0
        
        with open(self.filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return sum(1 for row in reader) - 1  # Subtract header


class ResumeManager:
    """Manages resume state for pagination"""
    
    def __init__(self, filename):
        self.filename = filename
        self.filepath = OUTPUT_DIR / filename
    
    def read_resume_page(self):
        """Read the last processed page number"""
        if self.filepath.exists():
            with open(self.filepath, "r") as f:
                return int(f.read().strip())
        return 1
    
    def write_resume_page(self, page):
        """Write the current page number"""
        with open(self.filepath, "w") as f:
            f.write(str(page))
