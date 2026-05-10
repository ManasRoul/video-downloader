# Step-by-Step Installation Guide

## Prerequisites

Before you begin, ensure you have:
- Ubuntu 18.04 or later (or Debian-based Linux distribution)
- Internet connection
- Terminal access
- sudo privileges

---

## Step 1: Transfer Files to Ubuntu

If you created this on macOS, transfer the entire `media-downloader` folder to your Ubuntu machine:

```bash
# Option A: Using SCP
scp -r /path/to/media-downloader user@ubuntu-machine:/home/user/

# Option B: Using USB drive, cloud storage, or Git
# Just copy the entire media-downloader folder to your Ubuntu system
```

For this guide, we'll assume the folder is at:
```
/home/YOUR_USERNAME/media-downloader
```

---

## Step 2: Open Terminal on Ubuntu

1. Press `Ctrl + Alt + T` to open a terminal
2. Navigate to the project directory:

```bash
cd ~/media-downloader
# or
cd /home/YOUR_USERNAME/media-downloader
```

---

## Step 3: Install System Dependencies

Install required system packages:

```bash
# Update package list
sudo apt-get update

# Install required packages (this may take a few minutes)
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-gi \
    python3-cairo \
    gir1.2-gtk-3.0 \
    gir1.2-appindicator3-0.1 \
    libnotify-bin \
    ffmpeg
```

**⚠️ Important:** Installing `python3-gi` and `python3-cairo` from apt is critical - do not try to install PyGObject via pip!

**What this installs:**
- `python3` - Python programming language
- `python3-pip` - Python package installer
- `python3-gi` - GTK bindings for Python (PyGObject)
- `python3-cairo` - Cairo graphics library bindings
- `gir1.2-gtk-3.0` - GTK 3 library
- `gir1.2-appindicator3-0.1` - System tray support
- `libnotify-bin` - Desktop notifications
- `ffmpeg` - Video/audio processing

**Expected output:** You should see packages being downloaded and installed.

---

## Step 4: Install Python Dependencies

Install required Python packages. **Choose the method based on your Ubuntu version:**

### Method A: For Ubuntu 23.04+ / Debian 12+ (Recommended)

Modern Ubuntu/Debian systems use "externally managed" Python. Use a virtual environment:

```bash
# Install python3-venv if not already installed
sudo apt-get install python3-venv python3-full

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install packages in the virtual environment
pip install -r requirements.txt
```

**Important:** When you run the application, use:
```bash
source venv/bin/activate  # Activate venv first
python main.py            # Then run the app
```

Or create a wrapper script (see Step 4b below).

### Method B: For Ubuntu 22.04 and earlier (System-wide with --user)

```bash
pip3 install --user -r requirements.txt
```

### Method C: Install System Packages (Alternative)

Some packages are available via apt:

```bash
sudo apt-get install -y \
    python3-requests \
    python3-websocket \
    python3-psutil

# Still need to install yt-dlp via pip (with --user or venv)
pip3 install --user yt-dlp
```

**What this installs:**
- yt-dlp - Media downloader
- requests - HTTP library
- websocket-client - WebSocket support
- psutil - System utilities

**Note:** PyGObject and pycairo are NOT installed via pip - they were already installed from apt in Step 3. This is intentional because building them from source requires many development libraries.

**Expected output:**
```
Successfully installed yt-dlp-X.X.X requests-X.X.X ...
```

---

## Step 4b: Create Wrapper Script (If Using Virtual Environment)

If you used Method A (virtual environment), create a wrapper script:

```bash
cat > ~/media-downloader/run.sh << 'EOF'
#!/bin/bash
# Wrapper script to run with virtual environment

cd "$(dirname "$0")"
source venv/bin/activate
python main.py "$@"
EOF

chmod +x ~/media-downloader/run.sh
```

Now you can run the app with:
```bash
~/media-downloader/run.sh
```

---

## Step 5: Install yt-dlp Binary

Install the yt-dlp command-line tool:

```bash
sudo wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -O /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
```

**Verify installation:**
```bash
yt-dlp --version
```

**Expected output:** Version number like `2024.05.10`

---

## Step 6: Generate Browser Extension Icons

Create the icon files for the browser extension:

```bash
cd browser-extension/icons
python3 generate-icons-simple.py
cd ../..
```

**Expected output:**
```
Creating browser extension icons...
✓ Created icon16.png
✓ Created icon48.png
✓ Created icon128.png
Icons created successfully!
```

---

## Step 7: Test the Application

Run a quick test to ensure everything is working:

**If using virtual environment (Method A):**
```bash
source venv/bin/activate
python start.py
```

**If using --user install (Method B or C):**
```bash
python3 start.py
```

**Or use the wrapper script:**
```bash
./run.sh  # If you created it in Step 4b
```

**Expected output:**
```
==================================================
Media Downloader - Quick Start
==================================================

Checking dependencies...
✓ Python version OK
✓ notify-send found
✓ yt-dlp found
✓ GTK bindings OK
✓ yt-dlp module OK

All dependencies OK! Starting application...
```

**What should happen:**
1. A notification appears: "Media Downloader - Application started"
2. An icon appears in your system tray (top panel)
3. The terminal shows: "Application started successfully"

**If you see errors:** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## Step 8: Install Browser Extension

### For Chrome/Chromium/Edge:

1. **Open Extensions Page:**
   - Chrome: Navigate to `chrome://extensions/`
   - Edge: Navigate to `edge://extensions/`
   - Or: Menu → Extensions → Manage Extensions

2. **Enable Developer Mode:**
   - Toggle "Developer mode" switch in the top-right corner

3. **Load Extension:**
   - Click "Load unpacked" button
   - Navigate to `/home/YOUR_USERNAME/media-downloader/browser-extension`
   - Select the folder and click "Open"

4. **Verify Installation:**
   - You should see "Media Downloader Helper" in your extensions list
   - The extension icon should appear in your toolbar
   - Status should show: "✓ Connected to Media Downloader"

### For Firefox:

1. **Open Debugging Page:**
   - Navigate to `about:debugging`
   - Click "This Firefox" in the left sidebar

2. **Load Extension:**
   - Click "Load Temporary Add-on..."
   - Navigate to `/home/YOUR_USERNAME/media-downloader/browser-extension`
   - Select `manifest.json` file
   - Click "Open"

3. **Verify Installation:**
   - Extension should appear in the list
   - Click the extension icon in the toolbar
   - Status should show: "✓ Connected to Media Downloader"

**Note:** Firefox temporary extensions are removed when you close the browser. You'll need to reload it each time, or sign it for permanent installation.

---

## Step 9: Test the Complete System

### Test 1: Connection Test

1. Make sure the application is running (from Step 7)
2. Click the browser extension icon
3. You should see: "✓ Connected to Media Downloader"
4. Click "Test Connection" button
5. You should see a notification: "Media Detected - Test Video"

### Test 2: Real Download Test

1. Open YouTube in your browser: https://www.youtube.com/watch?v=dQw4w9WgXcQ
2. Click play on the video
3. Within a few seconds, you should see:
   - A desktop notification: "Media Detected - [Video Title]"
   - A download dialog window appears

4. In the download dialog:
   - Select format (e.g., "MP4 (Best Quality)")
   - Choose save location (default is ~/Downloads)
   - Click "Download"

5. Watch the progress bar
6. When complete, notification: "Download Complete - Saved to: [file path]"

---

## Step 10: Optional - Install as System Service (Auto-start)

If you want the application to start automatically when you log in:

### Option A: Use the Install Script

```bash
chmod +x install.sh
./install.sh
```

This will:
- Install the application to `~/.local/share/media-downloader`

**If using virtual environment:**
```bash
cat > ~/.config/autostart/media-downloader.desktop << EOF
[Desktop Entry]
Type=Application
Name=Media Downloader
Exec=$HOME/media-downloader/run.sh
Icon=download
Terminal=false
Categories=Network;Utility;
StartupNotify=false
EOF
```

**If using --user install:**
- Create a launcher in `~/.local/bin/media-downloader`
- Add desktop entry for auto-start
- Set up system integration

### Option B: Manual Auto-start

1. Create autostart directory:
```bash
mkdir -p ~/.config/autostart
```

2. Create autostart file:
```bash
cat > ~/.config/autostart/media-downloader.desktop << EOF
[Desktop Entry]
Type=Application
Name=Media Downloader
Exec=/usr/bin/python3 $HOME/media-downloader/main.py
Icon=download
Terminal=false
Categories=Network;Utility;
StartupNotify=false
EOF
```

3. Make it executable:
```bash
chmod +x ~/.config/autostart/media-downloader.desktop
```

4. **Log out and back in** - the application will start automatically

---

## Step 11: Configure Settings (Optional)

1. Click the Media Downloader icon in the system tray
2. Select "Settings"
3. Configure:
   - **Download Path:** Where files are saved (default: ~/Downloads)
   - **Default Video Quality:** best, 720p, or 480p
   - **Audio Format:** mp3, m4a, or ogg
   - **Show Notifications:** Enable/disable notifications
4. Click "Save"

---

## Verification Checklist

✅ **System dependencies installed** - No errors in Step 3
✅ **Python packages installed** - No errors in Step 4
✅ **yt-dlp working** - Version command shows output
✅ **Application starts** - System tray icon appears
✅ **Browser extension loaded** - Shows in extensions list
✅ **Extension connected** - Shows "✓ Connected" status
✅ **Test download works** - Can download a YouTube video
✅ **Notifications appear** - Desktop notifications show up

---

# If using venv:
cd ~/media-downloader && source venv/bin/activate && python main.py

# If using --user:
## Common Issues and Solutions

### Issue 1: System tray icon doesn't appear

**Ubuntu 22.04+:**
```bash
sudo apt-get install gnome-shell-extension-appindicator
gnome-extensions enable ubuntu-appindicators@ubuntu.com
# Log out and back in
```

### Issue 2: Extension shows "✗ Not connected"

**Solution:**"externally-managed-environment" error

**Solution:**
This is normal on Ubuntu 23.04+ / Debian 12+. Use one of these:

```bash
# Option 1: Virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 2: User install
pip3 install --user -r requirements.txt

# Option 3: System packages where available
sudo apt-get install python3-requests python3-websocket python3-psutil
pip3 install --user yt-dlp
```

### Issue 5: Permission denied errors

**Solution:**
```bash
# Make scripts executable
chmod +x install.sh uninstall.sh run.sh
chmod +x browser-extension/icons/generate-icons.sh

# If pip fails, use --user flag
### Issue 3: Downloads fail

**Solution:**
```bash
# Update yt-dlp
sudo yt-dlp -U

# Test manually
yt-dlp "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Issue 4: Permission denied errors

**Solution:**
```bash
# Make scripts executable
chmod +x install.sh uninstall.sh
chmod +x browser-extension/icons/generate-icons.sh

# Install Python packages locally
pip3 install --user -r requirements.txt
```

---

## Uninstalling

To completely remove the application:

```bash
cd ~/media-downloader
./uninstall.sh
```

Or manually:
```bash
# Remove installed files
rm -rf ~/.local/share/media-downloader
rm -f ~/.local/bin/media-downloader
rm -f ~/.local/share/applications/media-downloader.desktop
rm -f ~/.config/autostart/media-downloader.desktop

# Remove config (optional)
rm -rf ~/.config/media-downloader
```

---

## Next Steps

After successful installation:

1. **Read the documentation:**
   - [USAGE.md](USAGE.md) - Detailed usage examples
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Solutions to common problems

2. **Try different sites:**
   - YouTube
   - Vimeo
   - Dailymotion
   - Direct video URLs

3. **Experiment with formats:**
   - Different video qualities
   - Audio extraction
   - Various codecs

4. **Customize settings:**
   - Change download location
   - Adjust default quality
   - Configure notifications

---

## Getting Help

If you encounter issues:

1. Check the logs:
   ```bash
   tail -f ~/.local/share/media-downloader/media-downloader.log
   ```

2. Review [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

3. Make sure all dependencies are installed

4. Test yt-dlp directly: `yt-dlp --version`

5. Check extension console: Right-click extension → Inspect popup

---

## Summary

You now have:
- ✅ A background application monitoring for media playback
- ✅ A browser extension detecting videos/audio
- ✅ A complete download system with progress tracking
- ✅ Desktop notifications for user feedback
- ✅ Configurable settings for customization

**Enjoy downloading media from your browser!** 🎉
