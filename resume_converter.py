#!/usr/bin/env python3
"""
Markdown Resume to PDF Converter

A command-line tool to convert markdown resumes to professionally formatted PDF documents
with customizable fonts, styles, and layout options.
"""

import argparse
import sys
import json
from pathlib import Path
import markdown
from pdf_generator import PDFGenerator
from config import ConfigManager

def main():
    """Main entry point for the resume converter."""
    parser = argparse.ArgumentParser(
        description="Convert markdown resumes to PDF format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python resume_converter.py resume.md -o resume.pdf
  python resume_converter.py resume.md --config custom_config.json
  python resume_converter.py resume.md --font-size 11 --margin 1.0
        """
    )
    
    parser.add_argument(
        "input_file",
        help="Input markdown file path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file path (default: input_file.pdf)",
        default=None
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Configuration file path (JSON format)",
        default=None
    )
    
    parser.add_argument(
        "--font-family",
        help="Font family (e.g., Helvetica, Times-Roman)",
        default=None
    )
    
    parser.add_argument(
        "--font-size",
        type=int,
        help="Base font size in points",
        default=None
    )
    
    parser.add_argument(
        "--margin",
        type=float,
        help="Page margins in inches",
        default=None
    )
    
    parser.add_argument(
        "--page-size",
        help="Page size (A4, Letter, Legal)",
        choices=["A4", "Letter", "Legal"],
        default=None
    )
    
    parser.add_argument(
        "--line-height",
        type=float,
        help="Line height multiplier",
        default=None
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        # Validate input file
        input_path = Path(args.input_file)
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist.", file=sys.stderr)
            sys.exit(1)
        
        if not input_path.is_file():
            print(f"Error: '{input_path}' is not a file.", file=sys.stderr)
            sys.exit(1)
        
        # Determine output file path
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = input_path.with_suffix('.pdf')
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        config_manager = ConfigManager()
        
        if args.config:
            config_path = Path(args.config)
            if not config_path.exists():
                print(f"Error: Configuration file '{config_path}' does not exist.", file=sys.stderr)
                sys.exit(1)
            config_manager.load_config(config_path)
        
        # Apply command-line overrides
        cli_overrides = {}
        if args.font_family:
            cli_overrides['font_family'] = args.font_family
        if args.font_size:
            cli_overrides['font_size'] = args.font_size
        if args.margin:
            cli_overrides['margin'] = args.margin
        if args.page_size:
            cli_overrides['page_size'] = args.page_size
        if args.line_height:
            cli_overrides['line_height'] = args.line_height
        
        config_manager.apply_overrides(cli_overrides)
        
        if args.verbose:
            print(f"Input file: {input_path}")
            print(f"Output file: {output_path}")
            print(f"Configuration: {json.dumps(config_manager.get_config(), indent=2)}")
        
        # Read and parse markdown
        if args.verbose:
            print("Reading markdown file...")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except UnicodeDecodeError as e:
            print(f"Error: Unable to read file '{input_path}' as UTF-8: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error reading file '{input_path}': {e}", file=sys.stderr)
            sys.exit(1)
        
        if not markdown_content.strip():
            print("Error: Input file is empty.", file=sys.stderr)
            sys.exit(1)
        
        # Convert markdown to HTML
        if args.verbose:
            print("Parsing markdown...")
        
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.nl2br'
        ])
        html_content = md.convert(markdown_content)
        
        # Generate PDF
        if args.verbose:
            print("Generating PDF...")
        
        pdf_generator = PDFGenerator(config_manager.get_config())
        pdf_generator.generate_pdf(html_content, str(output_path))
        
        print(f"Successfully converted '{input_path}' to '{output_path}'")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
