#!/usr/bin/env python3
"""
Create simple test background images for testing the background image functionality.
"""

from PIL import Image, ImageDraw
import os

def create_test_images():
    """Create simple test background images."""
    
    # Create tests/images directory
    os.makedirs('tests/images', exist_ok=True)
    
    # Create top background image (header style)
    top_img = Image.new('RGB', (800, 150), color='#e3f2fd')
    draw = ImageDraw.Draw(top_img)
    
    # Add some simple geometric shapes
    draw.rectangle([0, 0, 800, 20], fill='#1976d2')
    draw.rectangle([0, 130, 800, 150], fill='#1976d2')
    
    # Add diagonal lines for texture
    for i in range(0, 800, 40):
        draw.line([(i, 20), (i+20, 130)], fill='#bbdefb', width=2)
    
    top_img.save('tests/images/header_bg.png')
    
    # Create bottom background image (footer style)
    bottom_img = Image.new('RGB', (800, 100), color='#f3e5f5')
    draw = ImageDraw.Draw(bottom_img)
    
    # Add footer design
    draw.rectangle([0, 0, 800, 10], fill='#7b1fa2')
    draw.rectangle([0, 90, 800, 100], fill='#7b1fa2')
    
    # Add some circles
    for i in range(50, 800, 100):
        draw.ellipse([i-10, 30, i+10, 50], fill='#e1bee7')
        draw.ellipse([i-5, 35, i+5, 45], fill='#ce93d8')
    
    bottom_img.save('tests/images/footer_bg.png')
    
    print("Created test background images:")
    print("- tests/images/header_bg.png")
    print("- tests/images/footer_bg.png")

if __name__ == "__main__":
    create_test_images()