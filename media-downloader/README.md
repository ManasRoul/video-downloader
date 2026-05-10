# Ubuntu Media Downloader

A background application for Ubuntu that detects media (video/audio) playback in browsers and allows easy downloading.

## Features

- Runs as a background service with system tray icon
- Detects media playback in browsers (Chrome, Firefox, Edge)
- Shows popup notification when media is detected
- Downloads video/audio with yt-dlp
- File save dialog integration
- Supports multiple media formats

## Requirements

- Ubuntu 18.04 or later
- Python 3.8+
- GTK 3.0
- Browser extension (included)

## Installation

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 libnotify-bin
```

2. Install Python dependencies:
```bash
# For Ubuntu 23.04+ / Debian 12+ (externally-managed Python):
pip3 install --user -r requirements.txt

# Or use a virtual environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Getting "externally-managed-environment" error?** See [FIX-PIP-ERROR.md](FIX-PIP-ERROR.md)

3. Install the browser extension:
   - Chrome/Edge: Load unpacked extension from `browser-extension/` folder
   - Firefox: Load temporary add-on from `browser-extension/` folder

4. Run the installer:
```bash
chmod +x install.sh
./install.sh
```

## Usage

1. Start the application:
```bash
python3 main.py
```

Or use the desktop entry after installation:
```bash
media-downloader
```

2. The application will run in the system tray
3. When you play media in your browser, you'll see a notification
4. Click "Download" to save the media file
5. Choose the save location and format

## Configuration

Edit `~/.config/media-downloader/config.json` to customize:
- Default download location
- Preferred video quality
- Audio format preferences
- Notification settings

## Uninstallation

```bash
./uninstall.sh
```

## License

MIT License
