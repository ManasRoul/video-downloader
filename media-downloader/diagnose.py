#!/usr/bin/env python3
"""
Diagnostic script to help troubleshoot installation issues
"""

import sys
import os
import subprocess
import platform

print("=" * 60)
print("Media Downloader - Diagnostic Report")
print("=" * 60)
print()

# System Information
print("📋 System Information:")
print(f"  OS: {platform.system()} {platform.release()}")
print(f"  Python: {sys.version}")
print(f"  Working Directory: {os.getcwd()}")
print()

# Check if we're in the right directory
print("📁 Directory Check:")
if os.path.exists("main.py") and os.path.exists("src/daemon.py"):
    print("  ✓ Correct directory (found main.py and src/)")
else:
    print("  ✗ Wrong directory! Please run from the project root:")
    print("    cd ~/Downloads/video-downloader/media-downloader")
    print("    python3 diagnose.py")
    sys.exit(1)
print()

# Check Python packages
print("📦 Python Package Check:")

packages = {
    'gi': 'python3-gi (via apt)',
    'cairo': 'python3-cairo (via apt)',
    'requests': 'requests (via pip)',
    'yt_dlp': 'yt-dlp (via pip)',
    'websocket': 'websocket-client (via pip)',
    'psutil': 'psutil (via pip)'
}

missing = []
for module, name in packages.items():
    try:
        __import__(module)
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ✗ {name} - MISSING")
        missing.append((module, name))

print()

# Check GTK specifically
print("🎨 GTK Check:")
try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import Gtk, AppIndicator3
    print("  ✓ GTK 3.0")
    print("  ✓ AppIndicator3")
except Exception as e:
    print(f"  ✗ GTK Error: {e}")
print()

# Check application modules
print("🔧 Application Module Check:")
app_modules = [
    'src.config',
    'src.daemon',
    'src.tray_icon',
    'src.download_dialog',
    'src.downloader',
    'src.settings_dialog',
    'src.websocket_server'
]

module_errors = []
for module in app_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except Exception as e:
        print(f"  ✗ {module} - ERROR: {str(e)[:50]}")
        module_errors.append((module, str(e)))

print()

# Check yt-dlp binary
print("🎬 yt-dlp Binary Check:")
try:
    result = subprocess.run(['yt-dlp', '--version'], 
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"  ✓ yt-dlp binary found (v{result.stdout.strip()})")
    else:
        print(f"  ✗ yt-dlp binary error: {result.stderr}")
except FileNotFoundError:
    print("  ✗ yt-dlp binary not found")
    print("    Install with:")
    print("    sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp")
    print("    sudo chmod a+rx /usr/local/bin/yt-dlp")
except subprocess.TimeoutExpired:
    print("  ✗ yt-dlp binary timeout")
print()

# Check for Python cache issues
print("🗑️  Python Cache Check:")
pycache_dirs = []
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        pycache_dirs.append(os.path.join(root, '__pycache__'))

if pycache_dirs:
    print(f"  Found {len(pycache_dirs)} __pycache__ directories")
    print("  If you have import issues, try clearing cache:")
    print("    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null")
else:
    print("  ✓ No cache directories (clean)")
print()

# Summary and recommendations
print("=" * 60)
print("📊 Summary:")
print("=" * 60)

if missing:
    print("\n⚠️  MISSING PACKAGES:")
    for module, name in missing:
        print(f"  - {name}")
    print("\nTo install missing packages:")
    print("  sudo apt-get install python3-gi python3-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1")
    print("  pip3 install --user yt-dlp requests websocket-client psutil")

if module_errors:
    print("\n⚠️  MODULE ERRORS:")
    for module, error in module_errors:
        print(f"  - {module}: {error[:80]}")
    print("\nTry clearing Python cache:")
    print("  find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null")
    print("  find . -type f -name '*.pyc' -delete")

if not missing and not module_errors:
    print("\n✅ All checks passed! You can run the application:")
    print("  python3 main.py")
else:
    print("\n❌ Please fix the issues above, then run:")
    print("  python3 diagnose.py")
    print("\nFor more help, see:")
    print("  - COMMON-ERRORS.md")
    print("  - TROUBLESHOOTING.md")
    print("  - INSTALL.md")

print()
