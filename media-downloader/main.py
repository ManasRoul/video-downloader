#!/usr/bin/env python3
"""
Media Downloader - Main Entry Point
Background application that detects and downloads media from browsers
"""

import sys
import os
import signal
import logging
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, GLib

from src.daemon import MediaDownloaderDaemon
from src.tray_icon import TrayIcon
from src.config import Config

# Set up logging
LOG_DIR = Path.home() / '.local' / 'share' / 'media-downloader'
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / 'media-downloader.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class MediaDownloaderApp:
    """Main application class"""
    
    def __init__(self):
        self.config = Config()
        self.daemon = None
        self.tray_icon = None
        
    def run(self):
        """Start the application"""
        logger.info("Starting Media Downloader application")
        
        # Initialize daemon
        self.daemon = MediaDownloaderDaemon(self.config)
        self.daemon.start()
        
        # Initialize tray icon
        self.tray_icon = TrayIcon(self.daemon, self.config)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Show startup notification
        self._show_startup_notification()
        
        # Start GTK main loop
        logger.info("Application started successfully")
        Gtk.main()
        
    def _signal_handler(self, signum, frame):
        """Handle termination signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.quit()
        
    def _show_startup_notification(self):
        """Show notification that app has started"""
        os.system('notify-send "Media Downloader" "Application started. Ready to detect media." -i download')
        
    def quit(self):
        """Quit the application"""
        logger.info("Shutting down application")
        if self.daemon:
            self.daemon.stop()
        if self.tray_icon:
            self.tray_icon.quit()
        Gtk.main_quit()


def main():
    """Main entry point"""
    app = MediaDownloaderApp()
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        app.quit()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
