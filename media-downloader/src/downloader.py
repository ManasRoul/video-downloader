"""Media downloader using yt-dlp"""

import logging
import os
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class MediaDownloader:
    """Handles downloading media using yt-dlp"""
    
    def __init__(self, config):
        self.config = config
        
    def download(self, url, save_path, format_choice, progress_callback=None):
        """
        Download media from URL
        
        Args:
            url: Media URL
            save_path: Directory to save file
            format_choice: Format selection from combo box
            progress_callback: Callback for progress updates (progress, status)
            
        Returns:
            (success, output_file_path)
        """
        logger.info(f"Starting download: {url}")
        logger.info(f"Format: {format_choice}, Save path: {save_path}")
        
        try:
            # Build yt-dlp command
            cmd = ['yt-dlp']
            
            # Set output template
            output_template = os.path.join(save_path, '%(title)s.%(ext)s')
            cmd.extend(['-o', output_template])
            
            # Format selection
            if 'Audio Only' in format_choice or format_choice.startswith('MP3'):
                cmd.extend(['-x', '--audio-format', 'mp3'])
            elif 'M4A' in format_choice:
                cmd.extend(['-x', '--audio-format', 'm4a'])
            elif 'OGG' in format_choice:
                cmd.extend(['-x', '--audio-format', 'vorbis'])
            elif '720p' in format_choice:
                cmd.extend(['-f', 'bestvideo[height<=720]+bestaudio/best[height<=720]'])
            elif '480p' in format_choice:
                cmd.extend(['-f', 'bestvideo[height<=480]+bestaudio/best[height<=480]'])
            elif 'WebM' in format_choice:
                cmd.extend(['-f', 'bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]'])
            else:
                # Best quality
                cmd.extend(['-f', 'bestvideo+bestaudio/best'])
            
            # Merge to MP4 if not audio only
            if 'Audio' not in format_choice and 'MP3' not in format_choice:
                cmd.extend(['--merge-output-format', 'mp4'])
            
            # Progress template
            cmd.extend(['--newline', '--no-colors'])
            
            # Add URL
            cmd.append(url)
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            # Run yt-dlp
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            output_file = None
            
            # Monitor progress
            for line in process.stdout:
                line = line.strip()
                logger.debug(line)
                
                if progress_callback:
                    # Parse progress
                    if '[download]' in line:
                        if '%' in line:
                            try:
                                # Extract percentage
                                parts = line.split()
                                for part in parts:
                                    if '%' in part:
                                        percentage = float(part.replace('%', ''))
                                        progress_callback(percentage / 100, f"Downloading... {part}")
                                        break
                            except ValueError:
                                pass
                        elif 'Destination:' in line:
                            progress_callback(0.0, "Starting download...")
                    elif '[Merger]' in line or '[ExtractAudio]' in line:
                        progress_callback(0.9, "Processing...")
                    elif 'has already been downloaded' in line:
                        progress_callback(1.0, "File already exists")
                        
                # Extract output filename
                if 'Destination:' in line:
                    output_file = line.split('Destination:')[1].strip()
                elif 'Merging formats into' in line:
                    output_file = line.split('into')[1].strip().strip('"')
                elif '[ExtractAudio] Destination:' in line:
                    output_file = line.split('Destination:')[1].strip()
            
            # Wait for completion
            return_code = process.wait()
            
            if return_code == 0:
                logger.info(f"Download successful: {output_file}")
                if progress_callback:
                    progress_callback(1.0, "Download complete!")
                return True, output_file
            else:
                logger.error(f"Download failed with return code {return_code}")
                return False, None
                
        except Exception as e:
            logger.error(f"Download error: {e}", exc_info=True)
            return False, None
