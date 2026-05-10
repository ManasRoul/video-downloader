"""Settings dialog"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SettingsDialog:
    """Settings configuration dialog"""
    
    def __init__(self, config):
        self.config = config
        
        self.dialog = Gtk.Dialog(
            title="Settings",
            flags=Gtk.DialogFlags.MODAL
        )
        self.dialog.set_default_size(400, 300)
        
        self._build_ui()
        
    def _build_ui(self):
        """Build the settings UI"""
        box = self.dialog.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        
        # Download path
        path_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        path_label = Gtk.Label(label="Download Path:")
        path_box.pack_start(path_label, False, False, 0)
        
        self.path_entry = Gtk.Entry()
        self.path_entry.set_text(self.config.get('download_path'))
        path_box.pack_start(self.path_entry, True, True, 0)
        
        browse_button = Gtk.Button(label="Browse...")
        browse_button.connect("clicked", self._on_browse_clicked)
        path_box.pack_start(browse_button, False, False, 0)
        box.pack_start(path_box, False, False, 0)
        
        # Video quality
        quality_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        quality_label = Gtk.Label(label="Default Video Quality:")
        quality_box.pack_start(quality_label, False, False, 0)
        
        self.quality_combo = Gtk.ComboBoxText()
        self.quality_combo.append_text("best")
        self.quality_combo.append_text("720p")
        self.quality_combo.append_text("480p")
        self.quality_combo.set_active_id(self.config.get('video_quality'))
        quality_box.pack_start(self.quality_combo, True, True, 0)
        box.pack_start(quality_box, False, False, 0)
        
        # Audio format
        audio_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        audio_label = Gtk.Label(label="Audio Format:")
        audio_box.pack_start(audio_label, False, False, 0)
        
        self.audio_combo = Gtk.ComboBoxText()
        self.audio_combo.append_text("mp3")
        self.audio_combo.append_text("m4a")
        self.audio_combo.append_text("ogg")
        self.audio_combo.set_active_id(self.config.get('audio_format'))
        audio_box.pack_start(self.audio_combo, True, True, 0)
        box.pack_start(audio_box, False, False, 0)
        
        # Notifications
        self.notifications_check = Gtk.CheckButton(label="Show notifications")
        self.notifications_check.set_active(self.config.get('show_notifications'))
        box.pack_start(self.notifications_check, False, False, 0)
        
        # Buttons
        self.dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.dialog.add_button("Save", Gtk.ResponseType.OK)
        
        box.show_all()
        
    def _on_browse_clicked(self, button):
        """Browse for download path"""
        chooser = Gtk.FileChooserDialog(
            title="Select Download Location",
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            buttons=(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
        )
        
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            self.path_entry.set_text(chooser.get_filename())
        
        chooser.destroy()
        
    def run(self):
        """Run the dialog and save settings if OK"""
        response = self.dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Save settings
            self.config.set('download_path', self.path_entry.get_text())
            self.config.set('video_quality', self.quality_combo.get_active_text())
            self.config.set('audio_format', self.audio_combo.get_active_text())
            self.config.set('show_notifications', self.notifications_check.get_active())
        
        self.dialog.destroy()
