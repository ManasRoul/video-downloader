# Browser Extension for Media Downloader

This browser extension works with the Media Downloader native application to detect media playback and enable easy downloading.

## Installation

### Chrome/Chromium/Edge

1. Open `chrome://extensions/` (or `edge://extensions/`)
2. Enable "Developer mode" in the top right
3. Click "Load unpacked"
4. Select the `browser-extension` folder
5. The extension icon should appear in your toolbar

### Firefox

1. Open `about:debugging`
2. Click "This Firefox"
3. Click "Load Temporary Add-on"
4. Navigate to the `browser-extension` folder and select `manifest.json`
5. The extension will be loaded (note: it will be removed when you close Firefox)

For permanent installation in Firefox, the extension needs to be signed. You can:
- Sign it yourself at https://addons.mozilla.org/developers/
- Or reinstall it each time you restart Firefox

## How It Works

1. The extension monitors web pages for media elements (video/audio tags)
2. When media starts playing, it detects the URL
3. It communicates with the native Media Downloader app via WebSocket (port 8765)
4. The native app shows a notification and download dialog

## Supported Sites

The extension works with:
- Direct media files (.mp4, .webm, .mp3, etc.)
- YouTube
- Vimeo  
- Dailymotion
- Twitch
- Any site with HTML5 video/audio players

## Connection Status

Click the extension icon to see:
- Green checkmark: Connected to native app
- Red X: Not connected (start the Media Downloader app)

## Troubleshooting

**Extension shows "Not connected"**
- Make sure the Media Downloader app is running
- Check that nothing is blocking port 8765
- Check the extension console for errors (right-click extension icon → Inspect popup)

**Media not detected**
- Try playing the video/audio
- Check if the site uses a custom player
- Some sites may use DRM or special streaming that can't be detected

**Permission warnings**
- The extension needs broad permissions to detect media on all sites
- It only monitors for media playback and doesn't collect any personal data
- All communication stays local (localhost only)

## Privacy

- All data stays on your computer
- The extension only communicates with the local native app
- No data is sent to external servers
- No browsing history is collected or stored
