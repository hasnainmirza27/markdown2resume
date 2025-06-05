# Configuration Files

This directory contains configuration presets for different resume styles and layouts.

## Available Configurations

### `default_config.json`
- Default settings used by the converter
- Single column layout with standard professional styling
- Helvetica font, 11pt size, A4 page

### `single_column_professional.json`
- Traditional single-column resume format
- Times-Roman font for classic appearance
- Generous spacing for readability

### `modern_two_column.json`
- Contemporary two-column design
- Compact spacing for more content
- 68/32 column split ideal for skills sidebar

### `two_column_config.json`
- Balanced two-column layout
- Times-Roman font with professional styling
- 68/32 column split with custom gap

## Using Configuration Files

```bash
# Use a specific configuration
python resume_converter.py resume.md --config configs/modern_two_column.json

# Override specific settings
python resume_converter.py resume.md --config configs/default_config.json --font-size 12
```

## Configuration Options

| Setting | Description | Values |
|---------|-------------|---------|
| `font_family` | Font family | `"Helvetica"`, `"Times-Roman"`, `"Courier"` |
| `font_size` | Base font size in points | `8-24` |
| `line_height` | Line spacing multiplier | `1.0-2.0` |
| `margin` | Page margins in inches | `0.5-2.0` |
| `page_size` | Paper size | `"A4"`, `"Letter"`, `"Legal"` |
| `layout.type` | Layout type | `"single"`, `"two-column"` |
| `layout.columns.left_width` | Left column percentage | `50-80` |
| `layout.columns.right_width` | Right column percentage | `20-50` |
| `layout.columns.gap` | Column gap in points | `10-40` |