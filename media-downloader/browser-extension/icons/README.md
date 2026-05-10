# Icon Files

This directory contains the extension icons.

## Generating Icons

If the PNG files are missing, you can generate them from the SVG:

```bash
chmod +x generate-icons.sh
./generate-icons.sh
```

This requires ImageMagick:
```bash
sudo apt-get install imagemagick
```

## Manual Creation

Alternatively, create these files manually:
- `icon16.png` - 16x16 pixels
- `icon48.png` - 48x48 pixels  
- `icon128.png` - 128x128 pixels

The icon should represent downloading/media (e.g., a download arrow with a play button).

## Using Your Own Icons

Replace the PNG files with your own designs. Make sure they are:
- Square aspect ratio
- Transparent background
- Clear and recognizable at small sizes
