#!/usr/bin/env python3
"""
Quick Start Script for Media Downloader
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    print("Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print("✓ Python version OK")
    
    # Check for required commands
    commands = ['notify-send', 'yt-dlp']
    for cmd in commands:
        if subprocess.run(['which', cmd], capture_output=True).returncode != 0:
            print(f"❌ {cmd} not found")
            return False
        print(f"✓ {cmd} found")
    
    # Check Python packages
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('AppIndicator3', '0.1')
        print("✓ GTK bindings OK")
    except (ImportError, ValueError) as e:
        print(f"❌ GTK bindings missing: {e}")
        return False
    
    try:
        import yt_dlp
        print("✓ yt-dlp module OK")
    except ImportError:
        print("❌ yt-dlp module missing")
        return False
    
    return True

def main():
    """Quick start with dependency checking"""
    print("=" * 50)
    print("Media Downloader - Quick Start")
    print("=" * 50)
    print()
    
    # Check if we're in the right directory
    if not Path('main.py').exists():
        print("Error: Please run this script from the media-downloader directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print()
        print("Missing dependencies detected!")
        print()
        print("To install, run:")
        print("  ./install.sh")
        print()
        print("Or install manually:")
        print("  sudo apt-get install python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 libnotify-bin")
        print("  pip3 install -r requirements.txt")
        print("  sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp")
        print("  sudo chmod a+rx /usr/local/bin/yt-dlp")
        sys.exit(1)
    
    print()
    print("All dependencies OK! Starting application...")
    print()
    print("Next steps:")
    print("1. Install the browser extension from 'browser-extension' folder")
    print("2. Play a video/audio in your browser")
    print("3. Click the download notification")
    print()
    print("Press Ctrl+C to stop the application")
    print()
    
    # Start the application
    try:
        subprocess.run([sys.executable, 'main.py'])
    except KeyboardInterrupt:
        print("\nApplication stopped")

if __name__ == '__main__':
    main()
