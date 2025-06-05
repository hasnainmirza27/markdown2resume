# Test Files

This directory contains test files and sample resumes for validating the resume converter functionality.

## Test Files

- `sample_resume.md` - Comprehensive single-column resume example
- `sample_two_column_resume.md` - Two-column resume with manual column break
- `test_runner.py` - Automated test suite for all functionality

## Running Tests

### Manual Testing
```bash
# Test single column layout
python resume_converter.py tests/sample_resume.md -o test_output.pdf

# Test two-column layout
python resume_converter.py tests/sample_two_column_resume.md --layout two-column -o test_two_column.pdf
```

### Automated Test Suite
```bash
# Run all tests
python tests/test_runner.py
```

## Output Files

Test outputs are generated in this directory with descriptive names:
- `output_single_column.pdf`
- `output_two_column_default.pdf`
- `output_two_column_70_30.pdf`
- `output_config_test.pdf`
- And more...