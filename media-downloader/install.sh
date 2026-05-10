#!/bin/bash
# Installation script for Media Downloader

set -e

echo "====================================="
echo "Media Downloader Installation"
echo "====================================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: This application is designed for Linux (Ubuntu)"
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Install it with: sudo apt-get install python3"
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-gi \
    gir1.2-gtk-3.0 \
    gir1.2-appindicator3-0.1 \
    libnotify-bin \
    ffmpeg

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install yt-dlp
echo "Installing yt-dlp..."
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# Create directories
echo "Creating directories..."
mkdir -p ~/.config/media-downloader
mkdir -p ~/.local/share/media-downloader
mkdir -p ~/.local/share/applications
mkdir -p ~/.local/bin

# Copy application files
echo "Installing application..."
INSTALL_DIR="$HOME/.local/share/media-downloader"
cp -r src "$INSTALL_DIR/"
cp main.py "$INSTALL_DIR/"

# Create executable script
cat > ~/.local/bin/media-downloader << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/media-downloader"
python3 main.py "$@"
EOF
chmod +x ~/.local/bin/media-downloader

# Create desktop entry
cat > ~/.local/share/applications/media-downloader.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Media Downloader
Comment=Download media from browsers
Exec=$HOME/.local/bin/media-downloader
Icon=download
Terminal=false
Categories=Network;Utility;
StartupNotify=false
EOF

# Create autostart entry
mkdir -p ~/.config/autostart
cp ~/.local/share/applications/media-downloader.desktop ~/.config/autostart/

echo ""
echo "====================================="
echo "Installation Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Install the browser extension from the 'browser-extension' folder"
echo "2. Start the application: media-downloader"
echo "3. Or log out and back in for autostart"
echo ""
echo "Browser extension installation:"
echo "  Chrome/Edge: chrome://extensions -> Load unpacked -> Select 'browser-extension' folder"
echo "  Firefox: about:debugging -> Load Temporary Add-on -> Select 'browser-extension/manifest.json'"
echo ""
