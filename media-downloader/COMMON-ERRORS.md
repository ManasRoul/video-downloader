# Common Errors and Quick Fixes

## Error: "cannot import name 'MediaDownloaderDaemon'"

**Problem:** Python can't find or import the daemon module.

**Quick Fix:**
```bash
# 1. Make sure you're in the project directory
cd ~/Downloads/video-downloader/media-downloader

# 2. Verify the files exist
ls -la src/daemon.py src/websocket_server.py

# 3. Test imports
python3 test_imports.py

# 4. Run the app
python3 main.py
```

**Root Causes:**
- Running from wrong directory (must run from project root)
- Corrupted Python cache files
- Missing files

**Deep Fix:**
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Re-test
python3 test_imports.py
```

---

## Error: "ModuleNotFoundError: No module named 'gi'"

**Fix:**
```bash
sudo apt-get install python3-gi python3-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

---

## Error: "ModuleNotFoundError: No module named 'yt_dlp'"

**Fix:**
```bash
pip3 install --user yt-dlp requests websocket-client psutil
```

---

## Error: "ModuleNotFoundError: No module named 'src'"

**Problem:** Running from wrong directory.

**Fix:**
```bash
# Must run from project root, not from inside src/
cd ~/Downloads/video-downloader/media-downloader
python3 main.py  # Good ✓

# NOT this:
cd src
python3 ../main.py  # Bad ✗
```

---

## Error: cairo/pkg-config errors during pip install

**Problem:** Trying to install PyGObject via pip in a venv without system packages.

**Fix - Option 1 (Recommended):**
```bash
# Don't use venv - use --user install
deactivate  # if in venv
rm -rf venv
pip3 install --user -r requirements.txt
python3 main.py
```

**Fix - Option 2:**
```bash
# Use venv with system packages
deactivate
rm -rf venv
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Error: "externally-managed-environment"

**Fix:**
```bash
pip3 install --user -r requirements.txt
```

Or see [FIX-PIP-ERROR.md](FIX-PIP-ERROR.md)

---

## App starts but no tray icon appears

**Ubuntu 22.04+:**
```bash
sudo apt-get install gnome-shell-extension-appindicator
gnome-extensions enable ubuntu-appindicators@ubuntu.com
# Log out and back in
```

---

## Browser extension shows "Not connected"

**Check:**
```bash
# 1. Is app running?
ps aux | grep "python.*main.py"

# 2. Is port 8765 in use?
sudo netstat -tlnp | grep 8765

# 3. Check logs
tail -f ~/.local/share/media-downloader/media-downloader.log
```

**Fix:**
```bash
# Start the app
cd ~/Downloads/video-downloader/media-downloader
python3 main.py
```

---

## Complete Clean Reinstall

If nothing works, start fresh:

```bash
cd ~/Downloads/video-downloader/media-downloader

# 1. Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
rm -rf venv

# 2. Reinstall system packages
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-gi \
    python3-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-appindicator3-0.1 \
    libnotify-bin \
    ffmpeg

# 3. Install Python packages
pip3 install --user -r requirements.txt

# 4. Install yt-dlp binary
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp

# 5. Test
python3 test_imports.py

# 6. Run
python3 main.py
```

---

## Still Having Issues?

1. Check your Ubuntu version:
   ```bash
   lsb_release -a
   ```

2. Check Python version (need 3.8+):
   ```bash
   python3 --version
   ```

3. Run import test and share output:
   ```bash
   python3 test_imports.py
   ```

4. Check logs:
   ```bash
   cat ~/.local/share/media-downloader/media-downloader.log
   ```
