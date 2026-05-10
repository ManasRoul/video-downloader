"""Background daemon that monitors for media detection"""

import logging
import threading
import json
from src.websocket_server import WebsocketServer

logger = logging.getLogger(__name__)


class MediaDownloaderDaemon:
    """Background service that listens for media detection from browser"""
    
    def __init__(self, config):
        self.config = config
        self.server = None
        self.server_thread = None
        self.running = False
        self.media_callback = None
        self.clients = []
        
    def start(self):
        """Start the background daemon"""
        logger.info("Starting media downloader daemon")
        self.running = True
        
        # Start WebSocket server for browser communication
        port = self.config.get('port', 8765)
        self.server = WebsocketServer(host='127.0.0.1', port=port)
        
        # Set up callbacks
        self.server.set_fn_new_client(self._on_client_connect)
        self.server.set_fn_client_left(self._on_client_disconnect)
        self.server.set_fn_message_received(self._on_message_received)
        
        # Start server in separate thread
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        
        logger.info(f"Daemon started, listening on port {port}")
        
    def _run_server(self):
        """Run WebSocket server"""
        try:
            self.server.run_forever()
        except Exception as e:
            logger.error(f"Server error: {e}", exc_info=True)
            
    def _on_client_connect(self, client, server):
        """Handle new client connection"""
        logger.info(f"Browser client connected: {client['id']}")
        self.clients.append(client)
        
    def _on_client_disconnect(self, client, server):
        """Handle client disconnection"""
        logger.info(f"Browser client disconnected: {client['id']}")
        if client in self.clients:
            self.clients.remove(client)
            
    def _on_message_received(self, client, server, message):
        """Handle message from browser"""
        try:
            data = json.loads(message)
            logger.info(f"Received message: {data}")
            
            if data.get('type') == 'media_detected':
                self._handle_media_detected(data)
            elif data.get('type') == 'ping':
                # Respond to ping
                server.send_message(client, json.dumps({'type': 'pong'}))
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {message}")
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            
    def _handle_media_detected(self, data):
        """Handle media detection event"""
        media_info = {
            'url': data.get('url'),
            'title': data.get('title', 'Unknown'),
            'type': data.get('mediaType', 'video'),
            'page_url': data.get('pageUrl'),
            'thumbnail': data.get('thumbnail')
        }
        
        logger.info(f"Media detected: {media_info['title']} ({media_info['url']})")
        
        # Trigger callback if set
        if self.media_callback:
            self.media_callback(media_info)
            
    def set_media_callback(self, callback):
        """Set callback for when media is detected"""
        self.media_callback = callback
        
    def stop(self):
        """Stop the daemon"""
        logger.info("Stopping daemon")
        self.running = False
        if self.server:
            self.server.shutdown_gracefully()
