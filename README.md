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

Make sure you have Python 3.6 or higher installed on your system.

### Required Dependencies

The script requires the following Python packages:
- `markdown` - For parsing markdown content
- `reportlab` - For PDF generation
- `pathlib` - For file path handling (included in Python 3.4+)

Install the dependencies using pip:

```bash
pip install markdown reportlab
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

## Examples

### Convert with Two Columns
```bash
# Create a two-column resume with 65% left, 35% right
python resume_converter.py resume.md --layout two-column -o resume_2col.pdf
