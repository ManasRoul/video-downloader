#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""

import sys
import os

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("Testing imports...")
print(f"Working directory: {os.getcwd()}")
print("-" * 50)

# Test 1: Import gi (PyGObject)
try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import Gtk, AppIndicator3
    print("✓ GTK/AppIndicator imports OK")
except ImportError as e:
    print(f"✗ GTK import failed: {e}")
    print("  Fix: sudo apt-get install python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1")
    sys.exit(1)

# Test 2: Import standard packages
try:
    import requests
    print("✓ requests import OK")
except ImportError:
    print("✗ requests not found - run: pip3 install --user requests")
    sys.exit(1)

try:
    import yt_dlp
    print("✓ yt-dlp import OK")
except ImportError:
    print("✗ yt-dlp not found - run: pip3 install --user yt-dlp")
    sys.exit(1)

try:
    import websocket
    print("✓ websocket-client import OK")
except ImportError:
    print("✗ websocket-client not found - run: pip3 install --user websocket-client")
    sys.exit(1)

try:
    import psutil
    print("✓ psutil import OK")
except ImportError:
    print("✗ psutil not found - run: pip3 install --user psutil")
    sys.exit(1)

# Test 3: Import application modules
try:
    from src.config import Config
    print("✓ src.config import OK")
except ImportError as e:
    print(f"✗ src.config import failed: {e}")
    sys.exit(1)

try:
    from src.daemon import MediaDownloaderDaemon
    print("✓ src.daemon import OK")
except ImportError as e:
    print(f"✗ src.daemon import failed: {e}")
    sys.exit(1)

try:
    from src.tray_icon import TrayIcon
    print("✓ src.tray_icon import OK")
except ImportError as e:
    print(f"✗ src.tray_icon import failed: {e}")
    sys.exit(1)

try:
    from src.download_dialog import DownloadDialog
    print("✓ src.download_dialog import OK")
except ImportError as e:
    print(f"✗ src.download_dialog import failed: {e}")
    sys.exit(1)

try:
    from src.downloader import MediaDownloader
    print("✓ src.downloader import OK")
except ImportError as e:
    print(f"✗ src.downloader import failed: {e}")
    sys.exit(1)

try:
    from src.settings_dialog import SettingsDialog
    print("✓ src.settings_dialog import OK")
except ImportError as e:
    print(f"✗ src.settings_dialog import failed: {e}")
    sys.exit(1)

try:
    from src.websocket_server import WebsocketServer
    print("✓ src.websocket_server import OK")
except ImportError as e:
    print(f"✗ src.websocket_server import failed: {e}")
    sys.exit(1)

# Test 4: Check yt-dlp binary
import subprocess
try:
    result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✓ yt-dlp binary OK (version: {result.stdout.strip()})")
    else:
        print("✗ yt-dlp binary not working")
except FileNotFoundError:
    print("✗ yt-dlp binary not found")
    print("  Fix: sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp")
    print("       sudo chmod a+rx /usr/local/bin/yt-dlp")

print("-" * 50)
print("✓ All imports successful!")
print()
print("You can now run the application with:")
print("  python3 main.py")
