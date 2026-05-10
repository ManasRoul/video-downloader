# Quick Setup Guide

## For Ubuntu Users

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-gi \
    gir1.2-gtk-3.0 \
    gir1.2-appindicator3-0.1 \
    libnotify-bin \
    ffmpeg \
    imagemagick
```

### 2. Install Python Dependencies

```bash
cd media-downloader
pip3 install -r requirements.txt
```

### 3. Install yt-dlp

```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

### 4. Generate Browser Extension Icons

```bash
cd browser-extension/icons
python3 generate-icons.py
# or if you have ImageMagick:
# ./generate-icons.sh
cd ../..
```

### 5. Run the Application

```bash
python3 start.py
```

Or use the quick installer:

```bash
chmod +x install.sh
./install.sh
```

### 6. Install Browser Extension

#### Chrome/Edge:
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `browser-extension` folder

#### Firefox:
1. Open `about:debugging`
2. Click "This Firefox" → "Load Temporary Add-on"
3. Select `browser-extension/manifest.json`

## Testing

1. Start the application
2. Open YouTube in your browser
3. Play any video
4. You should see a notification
5. Click to download

## Troubleshooting

If the extension shows "Not connected":
- Make sure the app is running
- Check: `tail -f ~/.local/share/media-downloader/media-downloader.log`

If downloads fail:
- Test yt-dlp: `yt-dlp --version`
- Check permissions on Downloads folder

## Next Steps

- Configure settings via the tray icon
- Try different video sites (YouTube, Vimeo, etc.)
- Experiment with different format options
- Set custom download location

## Support

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed help.
