#!/bin/bash
# Generate PNG icons from SVG

if ! command -v convert &> /dev/null; then
    echo "ImageMagick is required to generate icons"
    echo "Install it with: sudo apt-get install imagemagick"
    exit 1
fi

cd "$(dirname "$0")"

echo "Generating PNG icons from SVG..."

# Generate different sizes
convert -background none icon.svg -resize 16x16 icon16.png
convert -background none icon.svg -resize 48x48 icon48.png
convert -background none icon.svg -resize 128x128 icon128.png

echo "Icons generated successfully!"
echo "Created: icon16.png, icon48.png, icon128.png"
