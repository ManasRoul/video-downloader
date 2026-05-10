"""
Simple WebSocket server for browser communication
"""

import socket
import threading
import hashlib
import base64
import struct
import logging

logger = logging.getLogger(__name__)


class WebsocketServer:
    """Simple WebSocket server for local communication"""
    
    def __init__(self, host='127.0.0.1', port=8765):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.running = False
        
        self.fn_new_client = None
        self.fn_client_left = None
        self.fn_message_received = None
        
    def set_fn_new_client(self, fn):
        self.fn_new_client = fn
        
    def set_fn_client_left(self, fn):
        self.fn_client_left = fn
        
    def set_fn_message_received(self, fn):
        self.fn_message_received = fn
        
    def run_forever(self):
        """Start the server"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        logger.info(f"WebSocket server listening on {self.host}:{self.port}")
        
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                logger.info(f"New connection from {address}")
                
                # Handle handshake in separate thread
                thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                thread.start()
            except Exception as e:
                if self.running:
                    logger.error(f"Server error: {e}")
                    
    def _handle_client(self, client_socket, address):
        """Handle WebSocket client"""
        try:
            # Perform WebSocket handshake
            handshake_data = client_socket.recv(1024).decode()
            
            # Extract WebSocket key
            key_line = [line for line in handshake_data.split('\n') if 'Sec-WebSocket-Key' in line]
            if not key_line:
                client_socket.close()
                return
                
            key = key_line[0].split(':')[1].strip()
            
            # Generate accept key
            magic = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
            accept_key = base64.b64encode(
                hashlib.sha1((key + magic).encode()).digest()
            ).decode()
            
            # Send handshake response
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
            )
            client_socket.send(response.encode())
            
            # Create client info
            client = {
                'id': len(self.clients) + 1,
                'socket': client_socket,
                'address': address
            }
            self.clients.append(client)
            
            # Call new client callback
            if self.fn_new_client:
                self.fn_new_client(client, self)
            
            # Listen for messages
            while self.running:
                try:
                    message = self._receive_message(client_socket)
                    if message:
                        if self.fn_message_received:
                            self.fn_message_received(client, self, message)
                    else:
                        break
                except Exception as e:
                    logger.error(f"Error receiving message: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Client handler error: {e}")
        finally:
            # Client disconnected
            if client in self.clients:
                self.clients.remove(client)
                if self.fn_client_left:
                    self.fn_client_left(client, self)
            client_socket.close()
            
    def _receive_message(self, client_socket):
        """Receive and decode WebSocket message"""
        try:
            # Read first 2 bytes
            data = client_socket.recv(2)
            if len(data) < 2:
                return None
                
            # Parse frame
            byte1, byte2 = struct.unpack('BB', data)
            
            # Check if message is masked (client to server should be masked)
            masked = byte2 & 0x80
            payload_length = byte2 & 0x7F
            
            # Get extended payload length if needed
            if payload_length == 126:
                data = client_socket.recv(2)
                payload_length = struct.unpack('>H', data)[0]
            elif payload_length == 127:
                data = client_socket.recv(8)
                payload_length = struct.unpack('>Q', data)[0]
            
            # Get masking key if masked
            if masked:
                masking_key = client_socket.recv(4)
            
            # Get payload
            payload = client_socket.recv(payload_length)
            
            # Unmask if needed
            if masked:
                payload = bytes([payload[i] ^ masking_key[i % 4] for i in range(len(payload))])
            
            return payload.decode('utf-8')
            
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            return None
            
    def send_message(self, client, message):
        """Send message to client"""
        try:
            # Encode message
            message_bytes = message.encode('utf-8')
            
            # Build frame
            frame = bytearray([0x81])  # Text frame
            
            length = len(message_bytes)
            if length <= 125:
                frame.append(length)
            elif length <= 65535:
                frame.append(126)
                frame.extend(struct.pack('>H', length))
            else:
                frame.append(127)
                frame.extend(struct.pack('>Q', length))
            
            frame.extend(message_bytes)
            
            client['socket'].send(frame)
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            
    def shutdown_gracefully(self):
        """Shutdown the server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
