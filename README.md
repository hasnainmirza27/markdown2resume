# Markdown Resume to PDF Converter

A Python command-line tool that converts markdown-formatted resumes into professionally styled PDF documents with customizable fonts, layouts, and styling options.

## Features

- **Markdown Support**: Full support for standard markdown syntax including headers, lists, bold, italic, and links
- **Customizable Styling**: Configure fonts, sizes, colors, and spacing
- **Professional Output**: Clean, readable PDF format suitable for job applications
- **Command-Line Interface**: Easy to use from the command line with various options
- **Configuration Files**: Support for JSON configuration files for consistent styling
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

Make sure you have Python 3.6 or higher installed on your system.

### Required Dependencies

The script requires the following Python packages:
- `markdown` - For parsing markdown content
- `reportlab` - For PDF generation
- `pathlib` - For file path handling (included in Python 3.4+)

Install the dependencies using pip:

```bash
pip install markdown reportlab
