#!/bin/bash
# Uninstallation script for Media Downloader

set -e

echo "====================================="
echo "Media Downloader Uninstallation"
echo "====================================="
echo ""

# Remove application files
echo "Removing application files..."
rm -rf ~/.local/share/media-downloader
rm -f ~/.local/bin/media-downloader
rm -f ~/.local/share/applications/media-downloader.desktop
rm -f ~/.config/autostart/media-downloader.desktop

# Ask about config and logs
read -p "Remove configuration and logs? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf ~/.config/media-downloader
    rm -rf ~/.local/share/media-downloader
    echo "Configuration and logs removed"
fi

echo ""
echo "====================================="
echo "Uninstallation Complete!"
echo "====================================="
echo ""
echo "Note: Browser extension must be removed manually"
echo "Python packages and system dependencies were not removed"
echo ""
