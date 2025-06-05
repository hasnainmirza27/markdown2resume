# Markdown Resume to PDF Converter

A Python command-line tool that converts markdown-formatted resumes into professionally styled PDF documents with customizable fonts, layouts, and styling options.

## Features

- **Markdown Support**: Full support for standard markdown syntax including headers, lists, bold, italic, and links
- **Two Layout Types**: Single-column and two-column layouts with customizable column widths
- **Customizable Styling**: Configure fonts, sizes, colors, spacing, and column proportions
- **Professional Output**: Clean, readable PDF format suitable for job applications
- **Command-Line Interface**: Easy to use from the command line with various options
- **Configuration Files**: Support for JSON configuration files for consistent styling
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Quick Installation

#### Option 1: Automated Installation (Recommended)
```bash
python install.py
```

#### Option 2: Manual Installation
```bash
pip install markdown reportlab
```

#### Option 3: Using Dependencies File
```bash
pip install -r dependencies.txt
```

### Verify Installation
```bash
python resume_converter.py --help
```

## Usage

### Basic Usage

Convert a markdown resume to PDF:

```bash
python resume_converter.py your_resume.md
```

### Single Column Layout (Default)

```bash
# Basic single column
python resume_converter.py resume.md -o resume.pdf

# With custom styling
python resume_converter.py resume.md --font-size 12 --margin 0.8 --page-size Letter
```

### Two Column Layout

Create a two-column resume with customizable column widths:

```bash
# Two-column with default widths (65% left, 35% right)
python resume_converter.py resume.md --layout two-column

# Custom column widths (must add up to 100%)
python resume_converter.py resume.md --layout two-column --left-width 70 --right-width 30

# With custom gap between columns
python resume_converter.py resume.md --layout two-column --left-width 60 --right-width 40 --column-gap 25
```

### Column Break Control

For two-column layouts, you can control where content splits between columns by adding a column break marker in your markdown:

```markdown
# Left Column Content

## Experience
Content for the left column...

<div class="column-break"></div>

## Skills
This content will start in the right column...
```

### Advanced Configuration

Use a configuration file for complex styling:

```bash
python resume_converter.py resume.md --config my_config.json
```

Example configuration file (`my_config.json`):

```json
{
  "font_family": "Times-Roman",
  "font_size": 11,
  "line_height": 1.3,
  "margin": 0.75,
  "page_size": "A4",
  "layout": {
    "type": "two-column",
    "columns": {
      "left_width": 65,
      "right_width": 35,
      "gap": 20
    }
  },
  "colors": {
    "heading": "#2c3e50",
    "text": "#000000",
    "link": "#3498db"
  }
}
```

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `input_file` | Input markdown file (required) | `resume.md` |
| `-o, --output` | Output PDF file path | `-o my_resume.pdf` |
| `-c, --config` | Configuration file path | `--config style.json` |
| `--font-family` | Font family | `--font-family "Times-Roman"` |
| `--font-size` | Base font size in points | `--font-size 12` |
| `--margin` | Page margins in inches | `--margin 1.0` |
| `--page-size` | Page size (A4, Letter, Legal) | `--page-size Letter` |
| `--line-height` | Line height multiplier | `--line-height 1.3` |
| `--layout` | Layout type (single, two-column) | `--layout two-column` |
| `--left-width` | Left column width percentage | `--left-width 70` |
| `--right-width` | Right column width percentage | `--right-width 30` |
| `--column-gap` | Gap between columns in points | `--column-gap 25` |
| `-v, --verbose` | Enable verbose output | `-v` |

## Layout Examples

### Single Column Layout
Perfect for traditional resume formats with a clean, linear flow of information.

### Two Column Layout (65/35)
Ideal for highlighting key information in a sidebar:
- Left column: Experience, projects, education
- Right column: Skills, certifications, contact info

### Two Column Layout (60/40)
Balanced layout for resumes with substantial sidebar content:
- More space for skills and additional information
- Good for technical resumes with extensive skill lists

## Column Width Guidelines

When using two-column layouts, column widths must always add up to 100%:

- **70/30**: Heavy emphasis on main content
- **65/35**: Standard professional layout (default)
- **60/40**: Balanced content distribution
- **55/45**: Equal emphasis on both columns

## Project Structure

```
resume-converter/
├── resume_converter.py          # Main script
├── pdf_generator.py             # PDF generation engine
├── config.py                    # Configuration management
├── install.py                   # Automated installation script
├── dependencies.txt             # Dependency specifications
├── README.md                    # Main documentation
├── INSTALL.md                   # Installation guide
├── configs/                     # Configuration presets
│   ├── default_config.json      # Default settings
│   ├── single_column_professional.json
│   ├── modern_two_column.json
│   ├── two_column_config.json
│   └── README.md
└── tests/                       # Test files and samples
    ├── sample_resume.md         # Sample single-column resume
    ├── sample_two_column_resume.md
    ├── test_runner.py           # Automated test suite
    └── README.md
```

## Quick Start Examples

### Basic Conversion
```bash
# Single column (default)
python resume_converter.py tests/sample_resume.md

# Two column with default settings
python resume_converter.py tests/sample_resume.md --layout two-column
```

### Using Configuration Presets
```bash
# Professional single-column style
python resume_converter.py resume.md --config configs/single_column_professional.json

# Modern two-column design
python resume_converter.py resume.md --config configs/modern_two_column.json
```

### Custom Column Layouts
```bash
# 70/30 split
python resume_converter.py resume.md --layout two-column --left-width 70 --right-width 30

# 60/40 split with custom gap
python resume_converter.py resume.md --layout two-column --left-width 60 --right-width 40 --column-gap 25
```

## Testing

### Run Test Suite
```bash
python tests/test_runner.py
```

### Manual Testing
```bash
# Test single column
python resume_converter.py tests/sample_resume.md -o output.pdf

# Test two column with column break
python resume_converter.py tests/sample_two_column_resume.md --layout two-column -o output_2col.pdf
