# Quick Fix: Python Installation Errors

## Error 1: "externally-managed-environment"

You're seeing this error because Ubuntu 23.04+ and Debian 12+ protect the system Python from conflicts.

## Error 2: PyGObject/pycairo build failures

If you see errors about "pkg-config", "cairo", or "meson" when installing, it means PyGObject is trying to build from source. **Don't do this!** Install it from apt instead.

**Fix:**
```bash
# Install GTK libraries from system packages
sudo apt-get install python3-gi python3-cairo gir1.2-gtk-3.0

# Then install only the other requirements
pip3 install --user yt-dlp requests websocket-client psutil
```

---

## ✅ Solution 1: Use Virtual Environment with System Packages (RECOMMENDED)

**⚠️ Important:** Regular venv isolates system packages. You need `--system-site-packages` to access python3-gi!

```bash
cd ~/media-downloader

# First install system GTK packages
sudo apt-get install -y python3-gi python3-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1

# Install venv support
sudo apt-get install python3-venv python3-full

# Create venv WITH access to system packages
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Now install only the pip packages
pip install -r requirements.txt

# Create wrapper script for easy running
cat > run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py "$@"
EOF

chmod +x run.sh

# Now run the app
./run.sh
```

**If you already created a venv without --system-site-packages:**
```bash
# Delete it and recreate
deactivate  # Exit venv first
rm -rf venv
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ✅ Solution 2: Install with --user Flag (SIMPLEST - NO VENV)

**This is actually the easiest method!** No virtual environment needed.

```bash
cd ~/media-downloader

# First ensure system packages are installed
sudo apt-get install -y python3-gi python3-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 libnotify-bin ffmpeg

# Install Python packages to user directory
pip3 install --user -r requirements.txt

# Run normally
python3 main.py
```

**Pros:** Simplest, no venv complexity, system packages work automatically
**Cons:** Packages installed globally for your user (but this is fine)

---

## ✅ Solution 3: System Packages + Minimal pip (HYBRID)

```bash
# Install what's available from Ubuntu repos
sudo apt-get install -y \
    python3-requests \
    python3-websocket \
    python3-psutil

# Only install yt-dlp via pip
pip3 install --user yt-dlp

# Run normally
python3 main.py
```
For simplicity**: Use Solution 2 (--user) ⭐ **RECOMMENDED**
- **For isolation**: Use Solution 1 (venv with --system-site-packages)
- **Avoid regular venv**: Don't use `python3 -m venv venv` without --system-site-packages (GTK won't work!)

**Why --user is recommended:**
- Works with system GTK packages automatically
- No venv complexity
- No activation/deactivation needed
- Just works!

- **Ubuntu 23.04+, Debian 12+**: Use Solution 1 (venv) or Solution 2 (--user)
- **Ubuntu 22.04 and earlier**: Use Solution 2 (--user) - simplest
- **Want isolation**: Use Solution 1 (venv)
- **Want simplicity**: Use Solution 2 (--user)

---

## Testing After Installation

Test that all imports work correctly:

```bash
# Run the import test
python3 test_imports.py
```

This will check all dependencies and show exactly what's missing.

Then try running the app:

```bash
# If using venv (Solution 1):
source venv/bin/activate
python main.py

# If using --user (Solution 2 or 3):
python3 main.py
```

You should see:
```
Checking dependencies...
✓ Python version OK
✓ notify-send found
✓ yt-dlp found
✓ GTK bindings OK
✓ yt-dlp module OK

All dependencies OK! Starting application...
```

---

## What NOT to Do

❌ **DO NOT USE:** `pip3 install --break-system-packages`
- This can break your system Python
- May cause Ubuntu updates to fail
- Not recommended by Ubuntu/Debian

---

## Need Help?

If you still have issues:

1. Check which Ubuntu version:
   ```bash
   lsb_release -a
   ```

2. Check Python version:
   ```bash
   python3 --version
   ```

3. See full installation guide: [INSTALL.md](INSTALL.md)
4. Check troubleshooting: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
