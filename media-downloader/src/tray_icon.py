"""System tray icon and menu"""

import logging
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

from .download_dialog import DownloadDialog

logger = logging.getLogger(__name__)


class TrayIcon:
    """System tray icon manager"""
    
    def __init__(self, daemon, config):
        self.daemon = daemon
        self.config = config
        
        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            "media-downloader",
            "download",
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        # Create menu
        self.menu = self._create_menu()
        self.indicator.set_menu(self.menu)
        
        # Set up media callback
        self.daemon.set_media_callback(self._on_media_detected)
        
        logger.info("Tray icon initialized")
        
    def _create_menu(self):
        """Create the tray menu"""
        menu = Gtk.Menu()
        
        # Status item
        self.status_item = Gtk.MenuItem(label="Ready")
        self.status_item.set_sensitive(False)
        menu.append(self.status_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Settings
        settings_item = Gtk.MenuItem(label="Settings")
        settings_item.connect("activate", self._on_settings_clicked)
        menu.append(settings_item)
        
        # About
        about_item = Gtk.MenuItem(label="About")
        about_item.connect("activate", self._on_about_clicked)
        menu.append(about_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit
        quit_item = Gtk.MenuItem(label="Quit")
        quit_item.connect("activate", self._on_quit_clicked)
        menu.append(quit_item)
        
        menu.show_all()
        return menu
        
    def _on_media_detected(self, media_info):
        """Handle media detection"""
        logger.info(f"Showing download dialog for: {media_info['title']}")
        
        # Show notification
        GLib.idle_add(self._show_notification, media_info)
        
        # Show download dialog
        GLib.idle_add(self._show_download_dialog, media_info)
        
    def _show_notification(self, media_info):
        """Show notification about detected media"""
        import os
        title = media_info.get('title', 'Unknown')
        media_type = media_info.get('type', 'media')
        os.system(f'notify-send "Media Detected" "{title}\nClick the tray icon to download this {media_type}." -i download -u normal')
        return False  # Don't repeat
        
    def _show_download_dialog(self, media_info):
        """Show download dialog"""
        dialog = DownloadDialog(media_info, self.config)
        dialog.run()
        return False  # Don't repeat
        
    def _on_settings_clicked(self, widget):
        """Show settings dialog"""
        from .settings_dialog import SettingsDialog
        dialog = SettingsDialog(self.config)
        dialog.run()
        
    def _on_about_clicked(self, widget):
        """Show about dialog"""
        about = Gtk.AboutDialog()
        about.set_program_name("Media Downloader")
        about.set_version("1.0.0")
        about.set_comments("Download media from your browser with ease")
        about.set_website("https://github.com/yourusername/media-downloader")
        about.set_logo_icon_name("download")
        about.run()
        about.destroy()
        
    def _on_quit_clicked(self, widget):
        """Quit the application"""
        self.quit()
        
    def update_status(self, status):
        """Update status text in menu"""
        self.status_item.set_label(status)
        
    def quit(self):
        """Clean up and quit"""
        logger.info("Quitting tray icon")
        Gtk.main_quit()
