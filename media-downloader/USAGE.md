# Usage Examples

## Example 1: Downloading a YouTube Video

1. Start the Media Downloader application:
   ```bash
   python3 main.py
   ```

2. Open your browser and navigate to a YouTube video (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)

3. Click play on the video

4. You'll see a system notification: "Media Detected - [Video Title]"

5. The download dialog will appear automatically with:
   - Video title
   - Video URL
   - Format options (MP4 Best Quality, MP4 720p, MP4 480p, WebM, Audio Only)
   - Save location

6. Select your preferred format and click "Download"

7. The video will download with a progress bar showing the status

8. When complete, you'll see: "Download Complete - Saved to: /path/to/file.mp4"

## Example 2: Downloading Audio from a Video

1. Start the application

2. Play any video in your browser

3. When the download dialog appears, select "Audio Only (MP3)"

4. Choose your save location

5. Click "Download"

6. The audio will be extracted and saved as an MP3 file

## Example 3: Changing Default Settings

1. Click the Media Downloader icon in your system tray

2. Select "Settings"

3. Modify:
   - Default download path
   - Preferred video quality
   - Audio format
   - Notification preferences

4. Click "Save"

5. New downloads will use these settings

## Example 4: Downloading from Vimeo

1. Navigate to a Vimeo video (e.g., https://vimeo.com/123456789)

2. Click play

3. The extension will detect the video and show a notification

4. Choose your format and download

## Example 5: Direct Media URL

If you have a direct link to a media file (e.g., https://example.com/video.mp4):

1. The extension will detect it when it starts playing

2. Or you can manually trigger detection by playing the media

3. Download as usual

## Command Line Testing

You can test yt-dlp directly:

```bash
# List available formats
yt-dlp -F "https://www.youtube.com/watch?v=VIDEO_ID"

# Download best quality
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# Download specific format
yt-dlp -f "best[height<=720]" "URL"

# Extract audio
yt-dlp -x --audio-format mp3 "URL"
```

## Troubleshooting Examples

### Extension not detecting media

```javascript
// Check browser console (F12)
// Look for messages from "Media Downloader Helper"

// Manually send test message
chrome.runtime.sendMessage({
  type: 'media_detected',
  url: 'https://example.com/test.mp4',
  title: 'Test Video',
  mediaType: 'video',
  pageUrl: window.location.href
});
```

### Application logs

```bash
# View real-time logs
tail -f ~/.local/share/media-downloader/media-downloader.log

# Search for errors
grep -i error ~/.local/share/media-downloader/media-downloader.log

# Check WebSocket connection
grep -i websocket ~/.local/share/media-downloader/media-downloader.log
```

### Testing WebSocket connection

```bash
# Check if port 8765 is listening
sudo netstat -tlnp | grep 8765

# Test WebSocket with wscat (if installed)
wscat -c ws://127.0.0.1:8765
# Send: {"type":"ping"}
# Expect: {"type":"pong"}
```

## Advanced Usage

### Custom Download Location per File

1. When the download dialog appears, click "Browse..."

2. Select a different folder for this specific download

3. The default location remains unchanged

### Batch Processing

While the application doesn't support queues yet, you can:

1. Play multiple videos in different tabs

2. Each will trigger a separate download dialog

3. Download them one at a time

### Integration with Other Tools

The downloaded files can be used with:

- Video editors (Kdenlive, Blender)
- Audio editors (Audacity)
- Media players (VLC)
- Cloud storage sync

## Tips and Tricks

1. **Faster Downloads**: Select a lower quality to download faster

2. **Save Space**: Use audio-only mode for music videos

3. **Organize Downloads**: Set up subfolders in your download directory

4. **Check Compatibility**: Not all sites are supported - test with yt-dlp first

5. **Keep Updated**: Update yt-dlp regularly for best results:
   ```bash
   sudo yt-dlp -U
   ```

6. **Monitor Performance**: Check system resources if downloads are slow

7. **Multiple Formats**: Download the same video in different formats by playing it multiple times
