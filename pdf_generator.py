"""
PDF Generator Module

Handles the conversion of HTML content to PDF using ReportLab with support for 
single-column and two-column layouts.
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4, legal
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import black, blue, darkblue, Color, HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, 
    PageBreak, FrameBreak, NextPageTemplate, KeepTogether, SimpleDocTemplate
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from html.parser import HTMLParser
import html

class HTMLToReportLabParser(HTMLParser):
    """Custom HTML parser to convert HTML to ReportLab flowables."""
    
    def __init__(self, styles, layout_config=None):
        super().__init__()
        self.styles = styles
        self.layout_config = layout_config or {'type': 'single'}
        self.flowables = []
        self.current_text = ""
        self.tag_stack = []
        self.list_level = 0
        self.list_items = []
        self.column_break_markers = []  # Track where column breaks should occur
        
    def handle_starttag(self, tag, attrs):
        """Handle opening HTML tags."""
        self.tag_stack.append(tag)
        
        # Check for column break markers (div with class="column-break")
        if tag == 'div':
            attrs_dict = dict(attrs)
            if attrs_dict.get('class') == 'column-break':
                self._flush_text()
                self.column_break_markers.append(len(self.flowables))
                return
        
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
    
    def get_flowables(self):
        """Finish parsing and return flowables."""
        self._flush_text()
        if self.list_items:
            self._add_list_items()
        
        # Insert column breaks for two-column layout
        if self.layout_config.get('type') == 'two-column':
            self._insert_column_breaks()
        
        return self.flowables
    
    def close(self):
        """Override parent close method."""
        super().close()
    
    def _insert_column_breaks(self):
        """Insert FrameBreak elements at column break markers."""
        for i, break_pos in enumerate(reversed(self.column_break_markers)):
            # Insert in reverse order to maintain positions
            self.flowables.insert(break_pos, FrameBreak())

class BackgroundPageTemplate(PageTemplate):
    """Custom page template with background support."""
    
    def __init__(self, id, frames, pagesize, background_config):
        super().__init__(id, frames, pagesize=pagesize)
        self.background_config = background_config
        self.pagesize = pagesize
    
    def beforeDrawPage(self, canv, doc):
        """Draw background before page content."""
        self._draw_background(canv)
    
    def _draw_background(self, canvas):
        """Draw the background based on configuration."""
        bg_config = self.background_config
        if not bg_config:
            return
        
        page_width, page_height = self.pagesize
        
        # Draw background color or gradient
        if bg_config.get('type') == 'gradient':
            self._draw_gradient(canvas, page_width, page_height, bg_config)
        else:
            self._draw_solid_background(canvas, page_width, page_height, bg_config)
        
        # Draw background images
        self._draw_background_images(canvas, page_width, page_height, bg_config)
    
    def _draw_solid_background(self, canvas, width, height, bg_config):
        """Draw solid background color."""
        color = bg_config.get('color', '#ffffff')
        try:
            bg_color = HexColor(color)
            canvas.setFillColor(bg_color)
            canvas.rect(0, 0, width, height, fill=1, stroke=0)
        except:
            # Fallback to white if color parsing fails
            canvas.setFillColor(HexColor('#ffffff'))
            canvas.rect(0, 0, width, height, fill=1, stroke=0)
    
    def _draw_gradient(self, canvas, width, height, bg_config):
        """Draw gradient background."""
        gradient_config = bg_config.get('gradient', {})
        start_color = gradient_config.get('start_color', '#ffffff')
        end_color = gradient_config.get('end_color', '#f8f9fa')
        fade_percentage = gradient_config.get('fade_percentage', 50)
        direction = gradient_config.get('direction', 'vertical')
        
        try:
            start_hex = HexColor(start_color)
            end_hex = HexColor(end_color)
            
            if direction == 'vertical':
                fade_point = height * (fade_percentage / 100)
                steps = 50  # Number of gradient steps
                
                for i in range(steps):
                    y = (height / steps) * i
                    if y <= fade_point:
                        # First part - start color to transition
                        ratio = y / fade_point if fade_point > 0 else 0
                    else:
                        # Second part - transition to end color
                        ratio = 1.0
                    
                    # Interpolate colors
                    r = start_hex.red + (end_hex.red - start_hex.red) * ratio
                    g = start_hex.green + (end_hex.green - start_hex.green) * ratio
                    b = start_hex.blue + (end_hex.blue - start_hex.blue) * ratio
                    
                    canvas.setFillColor(Color(r, g, b))
                    canvas.rect(0, y, width, height/steps, fill=1, stroke=0)
            else:
                # Horizontal gradient
                fade_point = width * (fade_percentage / 100)
                steps = 50
                
                for i in range(steps):
                    x = (width / steps) * i
                    if x <= fade_point:
                        ratio = x / fade_point if fade_point > 0 else 0
                    else:
                        ratio = 1.0
                    
                    r = start_hex.red + (end_hex.red - start_hex.red) * ratio
                    g = start_hex.green + (end_hex.green - start_hex.green) * ratio
                    b = start_hex.blue + (end_hex.blue - start_hex.blue) * ratio
                    
                    canvas.setFillColor(Color(r, g, b))
                    canvas.rect(x, 0, width/steps, height, fill=1, stroke=0)
                    
        except Exception:
            # Fallback to solid color if gradient fails
            self._draw_solid_background(canvas, width, height, bg_config)
    
    def _draw_background_images(self, canvas, width, height, bg_config):
        """Draw background images at top and bottom."""
        images_config = bg_config.get('images', {})
        if not images_config:
            return
        
        opacity = images_config.get('opacity', 0.1)
        top_image = images_config.get('top')
        bottom_image = images_config.get('bottom')
        
        # Draw top image
        if top_image and Path(top_image).exists():
            try:
                canvas.saveState()
                canvas.setFillAlpha(opacity)
                img = ImageReader(top_image)
                img_width, img_height = img.getSize()
                
                # Scale image to fit page width while maintaining aspect ratio
                scale = width / img_width
                scaled_height = img_height * scale
                
                # Position at top of page
                y_pos = height - scaled_height
                canvas.drawImage(img, 0, y_pos, width, scaled_height, mask='auto')
                canvas.restoreState()
            except Exception:
                pass  # Skip if image loading fails
        
        # Draw bottom image
        if bottom_image and Path(bottom_image).exists():
            try:
                canvas.saveState()
                canvas.setFillAlpha(opacity)
                img = ImageReader(bottom_image)
                img_width, img_height = img.getSize()
                
                # Scale image to fit page width while maintaining aspect ratio
                scale = width / img_width
                scaled_height = img_height * scale
                
                # Position at bottom of page
                canvas.drawImage(img, 0, 0, width, scaled_height, mask='auto')
                canvas.restoreState()
            except Exception:
                pass  # Skip if image loading fails

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
        styles['Normal'].alignment = TA_LEFT
        
        # Map font families to their bold variants
        font_mapping = {
            'Helvetica': 'Helvetica-Bold',
            'Times-Roman': 'Times-Bold',
            'Courier': 'Courier-Bold'
        }
        
        bold_font = font_mapping.get(font_family, f'{font_family}-Bold')
        
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
                    fontName=bold_font,
                    textColor=darkblue if i <= 2 else black,
                    alignment=TA_LEFT
                ))
            else:
                styles[style_name].fontName = bold_font
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
            layout_config = self.config.get('layout', {'type': 'single'})
            
            # Create styles
            styles = self._create_styles()
            
            # Preprocess HTML
            processed_html = self._preprocess_html(html_content)
            
            # Parse HTML to flowables
            parser = HTMLToReportLabParser(styles, layout_config)
            parser.feed(processed_html)
            flowables = parser.get_flowables()
            
            if not flowables:
                # If no flowables were generated, create a simple paragraph
                flowables = [Paragraph("No content to display", styles['Normal'])]
            
            # Create document based on layout type
            if layout_config.get('type') == 'two-column':
                self._build_two_column_pdf(output_path, page_size, margin, flowables, layout_config)
            else:
                self._build_single_column_pdf(output_path, page_size, margin, flowables)
            
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}")
    
    def _build_single_column_pdf(self, output_path, page_size, margin, flowables):
        """Build a single-column PDF with background support."""
        background_config = self.config.get('background', {})
        
        if background_config and background_config.get('type') != 'solid' or background_config.get('color') != '#ffffff':
            # Use BaseDocTemplate for background support
            doc = BaseDocTemplate(output_path, pagesize=page_size)
            
            # Create frame
            frame = Frame(
                margin, margin, 
                page_size[0] - 2 * margin, page_size[1] - 2 * margin,
                leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                id='single'
            )
            
            # Create page template with background
            page_template = BackgroundPageTemplate(
                id='SingleColumn', 
                frames=[frame], 
                pagesize=page_size,
                background_config=background_config
            )
            doc.addPageTemplates([page_template])
            doc.build(flowables)
        else:
            # Use SimpleDocTemplate for plain white background
            doc = SimpleDocTemplate(
                output_path,
                pagesize=page_size,
                leftMargin=margin,
                rightMargin=margin,
                topMargin=margin,
                bottomMargin=margin
            )
            doc.build(flowables)
    
    def _build_two_column_pdf(self, output_path, page_size, margin, flowables, layout_config):
        """Build a two-column PDF using BaseDocTemplate and frames with background support."""
        # Get column configuration
        columns = layout_config.get('columns', {})
        left_width_pct = columns.get('left_width', 65)
        right_width_pct = columns.get('right_width', 35)
        gap = columns.get('gap', 20)
        
        # Calculate dimensions
        page_width, page_height = page_size
        available_width = page_width - 2 * margin
        
        left_width = (available_width * left_width_pct / 100) - (gap / 2)
        right_width = (available_width * right_width_pct / 100) - (gap / 2)
        
        # Create frames
        left_frame = Frame(
            margin, margin, left_width, page_height - 2 * margin,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
            id='left'
        )
        
        right_frame = Frame(
            margin + left_width + gap, margin, right_width, page_height - 2 * margin,
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
            id='right'
        )
        
        # Create document and page template with background
        doc = BaseDocTemplate(output_path, pagesize=page_size)
        background_config = self.config.get('background', {})
        page_template = BackgroundPageTemplate(
            id='TwoColumn', 
            frames=[left_frame, right_frame],
            pagesize=page_size,
            background_config=background_config
        )
        doc.addPageTemplates([page_template])
        
        # Always auto-split for two-column layout (user can add manual breaks in markdown if needed)
        flowables = self._auto_split_columns(flowables)
        
        # Build PDF
        doc.build(flowables)
    
    def _auto_split_columns(self, flowables):
        """Automatically split content between columns."""
        # Simple heuristic: put roughly half the content in each column
        mid_point = len(flowables) // 2
        
        # Find a good break point (avoid breaking in the middle of a section)
        for i in range(max(0, mid_point - 5), min(len(flowables), mid_point + 5)):
            if i < len(flowables) and hasattr(flowables[i], '__class__') and flowables[i].__class__.__name__ == 'Spacer':
                mid_point = i + 1
                break
        
        # Insert frame break
        new_flowables = flowables[:mid_point] + [FrameBreak()] + flowables[mid_point:]
        return new_flowables
