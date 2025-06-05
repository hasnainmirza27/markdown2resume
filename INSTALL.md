# Installation Guide

## System Requirements

- **Python**: 3.6 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 50MB available space
- **Dependencies**: See below

## Installation Methods

### Method 1: Automated Installation (Recommended)

Run the installation script which will check your system and install all dependencies:

```bash
python install.py
```

This script will:
- Verify your Python version
- Install required packages (markdown, reportlab)
- Verify the installation
- Provide usage instructions

### Method 2: Manual Installation

If you prefer to install dependencies manually:

```bash
pip install markdown reportlab
```

### Method 3: Using Dependencies File

```bash
pip install -r dependencies.txt
```

## Verification

Test that everything is installed correctly:

```bash
# Check help
python resume_converter.py --help

# Test with sample file
python resume_converter.py tests/sample_resume.md -o test_output.pdf
```

## Troubleshooting

### Common Issues

**Python version too old:**
```
Error: Python 3.6 or higher is required
```
Solution: Upgrade Python or use a virtual environment with a newer version.

**Permission errors:**
```
PermissionError: [Errno 13] Permission denied
```
Solution: Use `pip install --user` or run with administrator privileges.

**Package conflicts:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```
Solution: Use a virtual environment:
```bash
python -m venv resume_env
source resume_env/bin/activate  # On Windows: resume_env\Scripts\activate
pip install markdown reportlab
```

### Virtual Environment Setup (Recommended)

Create an isolated environment for the project:

```bash
# Create virtual environment
python -m venv resume_converter_env

# Activate it
# On Windows:
resume_converter_env\Scripts\activate
# On macOS/Linux:
source resume_converter_env/bin/activate

# Install dependencies
pip install markdown reportlab

# Run the converter
python resume_converter.py tests/sample_resume.md
```

## Platform-Specific Notes

### Windows
- Use `python` command (may be `py` on some systems)
- Paths use backslashes: `tests\sample_resume.md`

### macOS/Linux
- May need `python3` instead of `python`
- Paths use forward slashes: `tests/sample_resume.md`

## Next Steps

After successful installation:

1. Read the main [README.md](README.md) for usage instructions
2. Try the sample files in the `tests/` folder
3. Explore configuration presets in the `configs/` folder
4. Run the test suite: `python tests/test_runner.py`