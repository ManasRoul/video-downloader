# Troubleshooting Guide

## Common Issues

### Application won't start

**Error: ModuleNotFoundError: No module named 'gi'**
```bash
sudo apt-get install python3-gi gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

**Error: No module named 'yt_dlp'**
```bash
pip3 install yt-dlp
```

**Error: yt-dlp command not found**
```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

### Browser Extension Issues

**Extension shows "Not connected"**
1. Make sure the Media Downloader app is running
2. Check if another app is using port 8765:
   ```bash
   sudo netstat -tlnp | grep 8765
   ```
3. Check the logs:
   ```bash
   tail -f ~/.local/share/media-downloader/media-downloader.log
   ```

**Media not being detected**
1. Try playing a video/audio file
2. Check the browser console (F12) for errors
3. Make sure the extension is enabled
4. Try reloading the page

**Extension not loading in Chrome**
1. Make sure Developer Mode is enabled
2. Try clicking "Pack extension" and loading the .crx file
3. Check chrome://extensions for any error messages

### Download Issues

**Download fails immediately**
1. Check if yt-dlp is installed: `yt-dlp --version`
2. Test manually: `yt-dlp <URL>`
3. Check write permissions on download folder
4. Check disk space

**Download is slow**
1. This is normal for large videos
2. Check your internet connection
3. Try selecting a lower quality format

**"Video unavailable" error**
1. The video may be region-locked
2. The video may require authentication
3. The site may have DRM protection
4. Update yt-dlp: `sudo yt-dlp -U`

### System Tray Icon not showing

**Ubuntu 22.04+**
1. Install GNOME Shell extension for tray icons:
   ```bash
   sudo apt-get install gnome-shell-extension-appindicator
   gnome-extensions enable ubuntu-appindicators@ubuntu.com
   ```
2. Log out and back in

**Other desktop environments**
- Make sure your system supports AppIndicator
- Try installing: `sudo apt-get install libappindicator3-1`

## Logs

Check application logs:
```bash
tail -f ~/.local/share/media-downloader/media-downloader.log
```

Check extension logs:
1. Right-click extension icon
2. Click "Inspect popup"
3. Go to Console tab

## Getting Help

If you're still having issues:

1. Check the logs (see above)
2. Try running with debug output:
   ```bash
   python3 main.py --debug
   ```
3. Create an issue on GitHub with:
   - Your Ubuntu version
   - Python version (`python3 --version`)
   - Error messages from logs
   - Steps to reproduce

## Performance

**High CPU usage**
- Normal during active download
- If high when idle, check logs for errors
- Try reducing video quality

**High memory usage**
- Normal for large video files
- Memory is released after download completes

## Uninstalling

To completely remove:
```bash
./uninstall.sh
# Remove Python packages
pip3 uninstall yt-dlp requests websocket-client psutil
# Remove system packages (optional)
sudo apt-get remove gir1.2-appindicator3-0.1
```
