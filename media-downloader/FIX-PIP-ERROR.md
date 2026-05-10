# Quick Fix: Python "externally-managed-environment" Error

You're seeing this error because Ubuntu 23.04+ and Debian 12+ protect the system Python from conflicts.

## ✅ Solution 1: Use Virtual Environment (RECOMMENDED)

```bash
cd ~/media-downloader

# Install venv support
sudo apt-get install python3-venv python3-full

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
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

**From now on, always run with:**
```bash
cd ~/media-downloader
./run.sh
```

---

## ✅ Solution 2: Install with --user Flag (SIMPLER)

```bash
cd ~/media-downloader

# Install to your user directory
pip3 install --user -r requirements.txt

# Run normally
python3 main.py
```

**Pros:** Simpler, no virtual environment needed
**Cons:** Packages installed globally for your user

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

---

## Which Method Should I Use?

- **Ubuntu 23.04+, Debian 12+**: Use Solution 1 (venv) or Solution 2 (--user)
- **Ubuntu 22.04 and earlier**: Use Solution 2 (--user) - simplest
- **Want isolation**: Use Solution 1 (venv)
- **Want simplicity**: Use Solution 2 (--user)

---

## Testing After Installation

```bash
# If using venv (Solution 1):
source venv/bin/activate
python start.py

# If using --user (Solution 2 or 3):
python3 start.py
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
