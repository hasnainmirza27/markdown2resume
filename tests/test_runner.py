#!/usr/bin/env python3
"""
Test Runner for Resume Converter

Runs various tests to validate the resume converter functionality across
different layouts, configurations, and styling options.
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ SUCCESS")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("✗ FAILED")
        print(f"Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Run all tests."""
    test_dir = Path(__file__).parent
    project_root = test_dir.parent
    
    tests = [
        # Single column tests
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_resume.md", "-o", "tests/output_single_column.pdf", "-v"],
            "desc": "Single Column Layout (Default)"
        },
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_resume.md", "--font-size", "12", "--margin", "0.8", "-o", "tests/output_custom_style.pdf", "-v"],
            "desc": "Single Column with Custom Styling"
        },
        
        # Two column tests
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_two_column_resume.md", "--layout", "two-column", "-o", "tests/output_two_column_default.pdf", "-v"],
            "desc": "Two Column Layout (Default 65/35)"
        },
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_resume.md", "--layout", "two-column", "--left-width", "70", "--right-width", "30", "-o", "tests/output_two_column_70_30.pdf", "-v"],
            "desc": "Two Column Layout (70/30)"
        },
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_resume.md", "--layout", "two-column", "--left-width", "60", "--right-width", "40", "--column-gap", "25", "-o", "tests/output_two_column_60_40.pdf", "-v"],
            "desc": "Two Column Layout (60/40 with custom gap)"
        },
        
        # Configuration file tests
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_two_column_resume.md", "--config", "configs/two_column_config.json", "-o", "tests/output_config_test.pdf", "-v"],
            "desc": "Configuration File Test"
        },
        
        # Different page sizes
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_resume.md", "--page-size", "Letter", "--layout", "two-column", "-o", "tests/output_letter_size.pdf", "-v"],
            "desc": "Letter Size Two Column"
        },
        
        # Font tests
        {
            "cmd": ["python", "resume_converter.py", "tests/sample_resume.md", "--font-family", "Times-Roman", "--font-size", "10", "-o", "tests/output_times_font.pdf", "-v"],
            "desc": "Times-Roman Font Test"
        }
    ]
    
    # Change to project root directory
    import os
    os.chdir(project_root)
    
    print("Resume Converter Test Suite")
    print("Testing various layouts, configurations, and styling options")
    
    passed = 0
    failed = 0
    
    for test in tests:
        if run_command(test["cmd"], test["desc"]):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {len(tests)}")
    
    if failed > 0:
        print("\nSome tests failed. Check the output above for details.")
        sys.exit(1)
    else:
        print("\nAll tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()