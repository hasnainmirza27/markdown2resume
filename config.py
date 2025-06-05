"""
Configuration Management Module

Handles loading and managing configuration for the PDF generator.
"""

import json
from pathlib import Path

class ConfigManager:
    """Manages configuration for the resume converter."""
    
    def __init__(self):
        """Initialize configuration manager with default settings."""
        self.config = self._get_default_config()
        self._load_default_config_file()
    
    def _get_default_config(self):
        """Get default configuration values."""
        return {
            "font_family": "Helvetica",
            "font_size": 11,
            "line_height": 1.2,
            "margin": 1.0,
            "page_size": "A4",
            "layout": {
                "type": "single",
                "columns": {
                    "left_width": 65,
                    "right_width": 35,
                    "gap": 20
                }
            },
            "colors": {
                "heading": "#1e3a8a",
                "text": "#000000",
                "link": "#2563eb"
            },
            "spacing": {
                "paragraph": 6,
                "heading": 12,
                "section": 18
            }
        }
    
    def _load_default_config_file(self):
        """Load default configuration file if it exists."""
        default_config_path = Path(__file__).parent / "default_config.json"
        if default_config_path.exists():
            try:
                self.load_config(default_config_path)
            except Exception:
                # If default config is invalid, stick with hardcoded defaults
                pass
    
    def load_config(self, config_path):
        """Load configuration from a JSON file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            
            # Merge with default config
            self._merge_config(user_config)
            
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in configuration file: {e}")
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {config_path}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")
    
    def _merge_config(self, user_config):
        """Merge user configuration with default configuration."""
        def merge_dict(default, user):
            """Recursively merge dictionaries."""
            for key, value in user.items():
                if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                    merge_dict(default[key], value)
                else:
                    default[key] = value
        
        merge_dict(self.config, user_config)
    
    def apply_overrides(self, overrides):
        """Apply command-line overrides to configuration."""
        for key, value in overrides.items():
            if value is not None:
                self.config[key] = value
    
    def get_config(self):
        """Get current configuration."""
        return self.config.copy()
    
    def validate_config(self):
        """Validate configuration values."""
        errors = []
        
        # Validate font size
        if not isinstance(self.config.get('font_size'), int) or self.config['font_size'] < 6:
            errors.append("Font size must be an integer >= 6")
        
        # Validate line height
        if not isinstance(self.config.get('line_height'), (int, float)) or self.config['line_height'] < 0.5:
            errors.append("Line height must be a number >= 0.5")
        
        # Validate margin
        if not isinstance(self.config.get('margin'), (int, float)) or self.config['margin'] < 0:
            errors.append("Margin must be a non-negative number")
        
        # Validate page size
        valid_page_sizes = ["A4", "Letter", "Legal"]
        if self.config.get('page_size') not in valid_page_sizes:
            errors.append(f"Page size must be one of: {', '.join(valid_page_sizes)}")
        
        # Validate layout configuration
        layout = self.config.get('layout', {})
        layout_type = layout.get('type')
        if layout_type not in ['single', 'two-column']:
            errors.append("Layout type must be 'single' or 'two-column'")
        
        if layout_type == 'two-column':
            columns = layout.get('columns', {})
            left_width = columns.get('left_width', 0)
            right_width = columns.get('right_width', 0)
            
            if not isinstance(left_width, (int, float)) or left_width <= 0:
                errors.append("Left column width must be a positive number")
            if not isinstance(right_width, (int, float)) or right_width <= 0:
                errors.append("Right column width must be a positive number")
            if left_width + right_width != 100:
                errors.append(f"Column widths must add up to 100% (got {left_width + right_width}%)")
            
            gap = columns.get('gap', 0)
            if not isinstance(gap, (int, float)) or gap < 0:
                errors.append("Column gap must be a non-negative number")
        
        if errors:
            raise Exception("Configuration validation failed:\n" + "\n".join(errors))
        
        return True
