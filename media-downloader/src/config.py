"""Configuration management for Media Downloader"""

import json
import os
from pathlib import Path


class Config:
    """Application configuration"""
    
    DEFAULT_CONFIG = {
        'download_path': str(Path.home() / 'Downloads'),
        'video_quality': 'best',
        'audio_format': 'mp3',
        'show_notifications': True,
        'auto_detect': True,
        'preferred_formats': ['mp4', 'webm', 'mkv'],
        'port': 8765
    }
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'media-downloader'
        self.config_file = self.config_dir / 'config.json'
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults to handle new keys
                return {**self.DEFAULT_CONFIG, **config}
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create config directory and file with defaults
            self.config_dir.mkdir(parents=True, exist_ok=True)
            self.save()
            return self.DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save()
    
    def get_download_path(self):
        """Get download path, create if doesn't exist"""
        path = Path(self.config['download_path'])
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
