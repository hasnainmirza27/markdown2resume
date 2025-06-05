#!/usr/bin/env python3
"""
Installation script for Markdown Resume to PDF Converter

This script installs the required dependencies for the resume converter.
"""

import subprocess
import sys
import platform

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"Installing {description}...")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ {description} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {description}")
        print(f"Error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print("Error: Python 3.6 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_dependencies():
    """Install required Python packages."""
    packages = [
        ("markdown", "Markdown parsing library"),
        ("reportlab", "PDF generation library")
    ]
    
    print("Installing Python dependencies...")
    
    for package, description in packages:
        cmd = [sys.executable, "-m", "pip", "install", package]
        if not run_command(cmd, description):
            return False
    
    return True

def verify_installation():
    """Verify that all dependencies are properly installed."""
    print("\nVerifying installation...")
    
    try:
        import markdown
        version = getattr(markdown, '__version__', 'unknown')
        print(f"✓ markdown {version}")
    except ImportError:
        print("✗ markdown not found")
        return False
    
    try:
        import reportlab
        version = getattr(reportlab, 'Version', 'unknown')
        print(f"✓ reportlab {version}")
    except ImportError:
        print("✗ reportlab not found")
        return False
    
    return True

def main():
    """Main installation process."""
    print("Markdown Resume to PDF Converter - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nInstallation failed. Please check the errors above.")
        sys.exit(1)
    
    # Verify installation
    if not verify_installation():
        print("\nInstallation verification failed.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("Installation completed successfully!")
    print("\nYou can now use the resume converter:")
    print("python resume_converter.py tests/sample_resume.md")
    print("\nFor help:")
    print("python resume_converter.py --help")

if __name__ == "__main__":
    main()