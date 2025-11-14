#!/usr/bin/env python3
import os
import glob
import subprocess

# Find all PDF files
for pdf_file in glob.glob("*.pdf"):
    # Create folder name (without .pdf extension)
    folder_name = pdf_file.replace(".pdf", "")
    
    # Create folder
    os.makedirs(folder_name, exist_ok=True)
    
    # Build and execute command
    cmd = [
        "/usr/bin/time", "-o", f"{folder_name}/timing.log",
        "./lockdownsl", "./pdftoppm",
        "-jpeg", "-jpegopt", "quality=50", "-r", "80",
        pdf_file, f"{folder_name}/pg"
    ]
    
    print(f"Processing: {pdf_file}")
    subprocess.run(cmd) 
