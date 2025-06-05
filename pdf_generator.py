"""
PDF Generator Module

Handles the conversion of HTML content to PDF using ReportLab.
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.lib.units import inch
from reportlab.lib.colors import black, blue, darkblue
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from html.parser import HTMLParser
import html

class HTMLToReportLabParser(HTMLParser):
    """Custom HTML parser to convert HTML to ReportLab flowables."""
    
    def __init__(self, styles):
        super().__init__()
        self.styles = styles
        self.flowables = []
        self.current_text = ""
        self.tag_stack = []
        self.list_level = 0
        self.list_items = []
        
    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags."""
        self.tag_stack.append(tag)
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._flush_text()
        elif tag == 'ul':
            self._flush_text()
            self.list_level += 1
        elif tag == 'ol':
            self._flush_text()
            self.list_level += 1
        elif tag == 'li':
            self._flush_text()
        elif tag == 'p':
            self._flush_text()
        elif tag == 'br':
            self.current_text += "<br/>"
        elif tag == 'strong' or tag == 'b':
            self.current_text += "<b>"
        elif tag == 'em' or tag == 'i':
            self.current_text += "<i>"
        elif tag == 'a':
            href = dict(attrs).get('href', '')
            if href:
                self.current_text += f'<link href="{href}" color="blue">'
            else:
                self.current_text += "<u>"
    
    def handle_endtag(self, tag):
        """Handle closing HTML tags."""
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if self.current_text.strip():
                style_name = f'Heading{tag[1]}'
                if style_name in self.styles:
                    para = Paragraph(self.current_text.strip(), self.styles[style_name])
                    self.flowables.append(para)
                    self.flowables.append(Spacer(1, 6))
            self.current_text = ""
        elif tag == 'ul' or tag == 'ol':
            self.list_level -= 1
            if self.list_level == 0:
                self._add_list_items()
        elif tag == 'li':
            if self.current_text.strip():
                self.list_items.append(self.current_text.strip())
            self.current_text = ""
        elif tag == 'p':
            if self.current_text.strip():
                para = Paragraph(self.current_text.strip(), self.styles['Normal'])
                self.flowables.append(para)
                self.flowables.append(Spacer(1, 6))
            self.current_text = ""
        elif tag == 'strong' or tag == 'b':
            self.current_text += "</b>"
        elif tag == 'em' or tag == 'i':
            self.current_text += "</i>"
        elif tag == 'a':
            self.current_text += "</link>"
    
    def handle_data(self, data):
        """Handle text data."""
        # Escape special characters and clean up whitespace
        cleaned_data = html.escape(data)
        cleaned_data = re.sub(r'\s+', ' ', cleaned_data)
        self.current_text += cleaned_data
    
    def _flush_text(self):
        """Flush any remaining text as a paragraph."""
        if self.current_text.strip():
            para = Paragraph(self.current_text.strip(), self.styles['Normal'])
            self.flowables.append(para)
            self.flowables.append(Spacer(1, 6))
        self.current_text = ""
    
    def _add_list_items(self):
        """Add accumulated list items to flowables."""
        for item in self.list_items:
            bullet_text = f"• {item}"
            para = Paragraph(bullet_text, self.styles['BulletList'])
            self.flowables.append(para)
        
        if self.list_items:
            self.flowables.append(Spacer(1, 6))
        self.list_items = []
    
    def close(self):
        """Finish parsing and return flowables."""
        self._flush_text()
        if self.list_items:
            self._add_list_items()
        super().close()
        return self.flowables

class PDFGenerator:
    """Main PDF generator class."""
    
    def __init__(self, config):
        """Initialize PDF generator with configuration."""
        self.config = config
        self.page_sizes = {
            'A4': A4,
            'Letter': letter,
            'Legal': legal
        }
    
    def _create_styles(self):
        """Create paragraph styles based on configuration."""
        styles = getSampleStyleSheet()
        
        # Base configuration
        font_family = self.config.get('font_family', 'Helvetica')
        base_font_size = self.config.get('font_size', 11)
        line_height = self.config.get('line_height', 1.2)
        
        # Normal paragraph style
        styles['Normal'].fontName = font_family
        styles['Normal'].fontSize = base_font_size
        styles['Normal'].leading = base_font_size * line_height
        styles['Normal'].spaceAfter = 6
        styles['Normal'].alignment = TA_JUSTIFY
        
        # Heading styles
        heading_sizes = [24, 20, 16, 14, 12, 11]
        for i in range(1, 7):
            style_name = f'Heading{i}'
            if style_name not in styles:
                styles.add(ParagraphStyle(
                    name=style_name,
                    parent=styles['Normal'],
                    fontSize=max(heading_sizes[i-1], base_font_size),
                    leading=max(heading_sizes[i-1], base_font_size) * 1.2,
                    spaceAfter=12,
                    spaceBefore=12,
                    fontName=f'{font_family}-Bold',
                    textColor=darkblue if i <= 2 else black,
                    alignment=TA_LEFT
                ))
            else:
                styles[style_name].fontName = f'{font_family}-Bold'
                styles[style_name].fontSize = max(heading_sizes[i-1], base_font_size)
                styles[style_name].leading = max(heading_sizes[i-1], base_font_size) * 1.2
                styles[style_name].textColor = darkblue if i <= 2 else black
        
        # Bullet list style
        styles.add(ParagraphStyle(
            name='BulletList',
            parent=styles['Normal'],
            leftIndent=20,
            spaceAfter=3,
            bulletIndent=5
        ))
        
        return styles
    
    def _preprocess_html(self, html_content):
        """Preprocess HTML content to handle special cases."""
        # Remove extra whitespace
        html_content = re.sub(r'\n\s*\n', '\n', html_content)
        html_content = re.sub(r'^\s+|\s+$', '', html_content, flags=re.MULTILINE)
        
        # Ensure paragraphs are properly wrapped
        lines = html_content.split('\n')
        processed_lines = []
        in_list = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with HTML tag
            if line.startswith('<'):
                processed_lines.append(line)
                if '<ul>' in line or '<ol>' in line:
                    in_list = True
                elif '</ul>' in line or '</ol>' in line:
                    in_list = False
            else:
                # Plain text line - wrap in paragraph if not in list
                if not in_list:
                    processed_lines.append(f'<p>{line}</p>')
                else:
                    processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def generate_pdf(self, html_content, output_path):
        """Generate PDF from HTML content."""
        try:
            # Get page configuration
            page_size = self.page_sizes.get(
                self.config.get('page_size', 'A4'), 
                A4
            )
            margin = self.config.get('margin', 1.0) * inch
            
            # Create document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=page_size,
                leftMargin=margin,
                rightMargin=margin,
                topMargin=margin,
                bottomMargin=margin
            )
            
            # Create styles
            styles = self._create_styles()
            
            # Preprocess HTML
            processed_html = self._preprocess_html(html_content)
            
            # Parse HTML to flowables
            parser = HTMLToReportLabParser(styles)
            parser.feed(processed_html)
            flowables = parser.close()
            
            if not flowables:
                # If no flowables were generated, create a simple paragraph
                flowables = [Paragraph("No content to display", styles['Normal'])]
            
            # Build PDF
            doc.build(flowables)
            
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")
