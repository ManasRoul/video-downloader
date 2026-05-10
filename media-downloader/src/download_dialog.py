"""Download dialog for media files"""

import logging
import os
from pathlib import Path
import threading

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from src.downloader import MediaDownloader

logger = logging.getLogger(__name__)


class DownloadDialog:
    """Dialog for downloading media"""
    
    def __init__(self, media_info, config):
        self.media_info = media_info
        self.config = config
        self.downloader = MediaDownloader(config)
        self.download_thread = None
        
        # Create dialog
        self.dialog = Gtk.Dialog(
            title="Download Media",
            flags=Gtk.DialogFlags.MODAL
        )
        self.dialog.set_default_size(500, 300)
        
        self._build_ui()
        
    def _build_ui(self):
        """Build the dialog UI"""
        box = self.dialog.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{self.media_info.get('title', 'Unknown')}</b>")
        title_label.set_line_wrap(True)
        box.pack_start(title_label, False, False, 0)
        
        # URL
        url_label = Gtk.Label(label=self.media_info.get('url', ''))
        url_label.set_line_wrap(True)
        url_label.set_selectable(True)
        box.pack_start(url_label, False, False, 0)
        
        # Separator
        box.pack_start(Gtk.Separator(), False, False, 5)
        
        # Format selection
        format_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        format_label = Gtk.Label(label="Format:")
        format_box.pack_start(format_label, False, False, 0)
        
        self.format_combo = Gtk.ComboBoxText()
        if self.media_info.get('type') == 'video':
            self.format_combo.append_text("MP4 (Best Quality)")
            self.format_combo.append_text("MP4 (720p)")
            self.format_combo.append_text("MP4 (480p)")
            self.format_combo.append_text("WebM")
            self.format_combo.append_text("Audio Only (MP3)")
        else:
            self.format_combo.append_text("MP3 (Best Quality)")
            self.format_combo.append_text("M4A")
            self.format_combo.append_text("OGG")
        self.format_combo.set_active(0)
        format_box.pack_start(self.format_combo, True, True, 0)
        box.pack_start(format_box, False, False, 0)
        
        # Save location
        location_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        location_label = Gtk.Label(label="Save to:")
        location_box.pack_start(location_label, False, False, 0)
        
        self.location_entry = Gtk.Entry()
        default_path = self.config.get_download_path()
        self.location_entry.set_text(default_path)
        location_box.pack_start(self.location_entry, True, True, 0)
        
        browse_button = Gtk.Button(label="Browse...")
        browse_button.connect("clicked", self._on_browse_clicked)
        location_box.pack_start(browse_button, False, False, 0)
        box.pack_start(location_box, False, False, 0)
        
        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_show_text(True)
        self.progress_bar.set_text("Ready to download")
        box.pack_start(self.progress_bar, False, False, 10)
        
        # Status label
        self.status_label = Gtk.Label(label="")
        box.pack_start(self.status_label, False, False, 0)
        
        # Buttons
        self.download_button = self.dialog.add_button("Download", Gtk.ResponseType.OK)
        self.cancel_button = self.dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        
        box.show_all()
        
    def _on_browse_clicked(self, button):
        """Handle browse button click"""
        chooser = Gtk.FileChooserDialog(
            title="Select Download Location",
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
        )
        
        current_path = self.location_entry.get_text()
        if os.path.exists(current_path):
            chooser.set_current_folder(current_path)
        
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            self.location_entry.set_text(chooser.get_filename())
        
        chooser.destroy()
        
    def _on_progress_update(self, progress, status):
        """Update progress bar"""
        GLib.idle_add(self._update_progress_ui, progress, status)
        
    def _update_progress_ui(self, progress, status):
        """Update UI elements with progress"""
        self.progress_bar.set_fraction(progress)
        self.progress_bar.set_text(f"{int(progress * 100)}%")
        self.status_label.set_text(status)
        return False
        
    def _start_download(self):
        """Start the download"""
        url = self.media_info['url']
        save_path = self.location_entry.get_text()
        format_choice = self.format_combo.get_active_text()
        
        # Disable buttons during download
        self.download_button.set_sensitive(False)
        self.cancel_button.set_label("Close")
        
        # Start download in thread
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, save_path, format_choice),
            daemon=True
        )
        self.download_thread.start()
        
    def _download_worker(self, url, save_path, format_choice):
        """Worker thread for downloading"""
        try:
            self._on_progress_update(0.0, "Starting download...")
            
            success, output_file = self.downloader.download(
                url, 
                save_path, 
                format_choice,
                progress_callback=self._on_progress_update
            )
            
            if success:
                self._on_progress_update(1.0, f"Download complete: {output_file}")
                GLib.idle_add(self._show_success_notification, output_file)
            else:
                self._on_progress_update(0.0, "Download failed")
                GLib.idle_add(self._show_error_notification)
                
        except Exception as e:
            logger.error(f"Download error: {e}", exc_info=True)
            self._on_progress_update(0.0, f"Error: {str(e)}")
            GLib.idle_add(self._show_error_notification)
            
    def _show_success_notification(self, output_file):
        """Show success notification"""
        os.system(f'notify-send "Download Complete" "Saved to: {output_file}" -i download')
        return False
        
    def _show_error_notification(self):
        """Show error notification"""
        os.system('notify-send "Download Failed" "Please check the logs for details." -i error')
        return False
        
    def run(self):
        """Run the dialog"""
        response = self.dialog.run()
        
        if response == Gtk.ResponseType.OK:
            self._start_download()
            # Keep dialog open to show progress
            while self.download_thread and self.download_thread.is_alive():
                Gtk.main_iteration_do(False)
        
        self.dialog.destroy()
