#!/usr/bin/env python3
import re
import os
from pathlib import Path
from collections import defaultdict

def get_functions_from_file_fast(filepath):
    """Extract function names from a Python file using regex (faster)."""
    functions = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # Find all function definitions
            pattern = r'^def\s+(\w+)\s*\('
            matches = re.findall(pattern, content, re.MULTILINE)
            functions = list(set(matches))  # Remove duplicates
    except Exception as e:
        pass
    return functions

def main():
    root_dir = Path("c:/Users/Admin/Downloads/revival project/revival project/script_patch")
    
    file_summary = {}
    total_files = 0
    files_with_functions = 0
    
    # Walk through all Python files
    py_files = sorted(list(root_dir.rglob("*.py")))
    print(f"Found {len(py_files)} files. Processing...")
    
    for i, py_file in enumerate(py_files):
        if i % 500 == 0:
            print(f"Processing... {i}/{len(py_files)}")
        
        total_files += 1
        rel_path = str(py_file.relative_to(root_dir))
        functions = get_functions_from_file_fast(py_file)
        
        if functions:
            file_summary[rel_path] = functions
            files_with_functions += 1
    
    # Write summary to file
    output_file = Path("c:/Users/Admin/Downloads/revival project/revival project/FILE_ANALYSIS_SUMMARY.txt")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 100 + "\n")
        f.write("REVIVAL PROJECT - FILE ANALYSIS SUMMARY\n")
        f.write("=" * 100 + "\n")
        f.write(f"\nTotal files analyzed: {total_files}\n")
        f.write(f"Files with functions: {files_with_functions}\n\n")
        
        for filepath in sorted(file_summary.keys()):
            functions = file_summary[filepath]
            f.write(f"\n{'-' * 100}\n")
            f.write(f"FILE: {filepath}\n")
            f.write(f"{'-' * 100}\n")
            f.write(f"Functions found: {len(functions)}\n")
            for func in sorted(functions):
                f.write(f"  - {func}\n")
    
    print(f"\n✓ Analysis complete!")
    print(f"Summary written to: {output_file}")
    print(f"Total files: {total_files}")
    print(f"Files with functions: {files_with_functions}")

if __name__ == "__main__":
    main()
