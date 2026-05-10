// Background service worker for media detection
console.log('Media Downloader Helper: Background script loaded');

let ws = null;
let reconnectInterval = 5000;
let isConnected = false;

// Connect to native application
function connectToNativeApp() {
  try {
    ws = new WebSocket('ws://127.0.0.1:8765');
    
    ws.onopen = () => {
      console.log('Connected to Media Downloader app');
      isConnected = true;
      chrome.action.setBadgeText({ text: '✓' });
      chrome.action.setBadgeBackgroundColor({ color: '#4CAF50' });
    };
    
    ws.onclose = () => {
      console.log('Disconnected from Media Downloader app');
      isConnected = false;
      chrome.action.setBadgeText({ text: '✗' });
      chrome.action.setBadgeBackgroundColor({ color: '#f44336' });
      
      // Reconnect after delay
      setTimeout(connectToNativeApp, reconnectInterval);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    ws.onmessage = (event) => {
      console.log('Message from app:', event.data);
    };
    
  } catch (error) {
    console.error('Failed to connect:', error);
    setTimeout(connectToNativeApp, reconnectInterval);
  }
}

// Send media info to native app
function sendMediaToApp(mediaInfo) {
  if (ws && isConnected) {
    try {
      ws.send(JSON.stringify({
        type: 'media_detected',
        ...mediaInfo
      }));
      console.log('Sent media info to app:', mediaInfo);
    } catch (error) {
      console.error('Failed to send media info:', error);
    }
  } else {
    console.warn('Not connected to app, cannot send media info');
  }
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Received message:', message);
  
  if (message.type === 'media_detected') {
    // Add tab info
    message.pageUrl = sender.tab?.url || message.pageUrl;
    message.pageTitle = sender.tab?.title || message.pageTitle;
    
    // Send to native app
    sendMediaToApp(message);
    
    sendResponse({ success: true });
  } else if (message.type === 'check_connection') {
    sendResponse({ connected: isConnected });
  }
  
  return true;
});

// Monitor web requests for media URLs
chrome.webRequest.onBeforeRequest.addListener(
  (details) => {
    const url = details.url;
    
    // Check if it's a media file
    const mediaExtensions = ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.m3u8', '.mp3', '.m4a', '.wav', '.ogg'];
    const isMediaFile = mediaExtensions.some(ext => url.toLowerCase().includes(ext));
    
    // Check for streaming platforms
    const streamingPlatforms = ['youtube.com', 'vimeo.com', 'dailymotion.com', 'twitch.tv'];
    const isStreamingPlatform = streamingPlatforms.some(platform => url.includes(platform));
    
    if (isMediaFile || isStreamingPlatform) {
      console.log('Media URL detected:', url);
      
      // Get tab info
      chrome.tabs.get(details.tabId, (tab) => {
        if (chrome.runtime.lastError) {
          console.error(chrome.runtime.lastError);
          return;
        }
        
        sendMediaToApp({
          url: url,
          title: tab.title || 'Unknown',
          type: url.includes('.mp3') || url.includes('.m4a') ? 'audio' : 'video',
          pageUrl: tab.url,
          thumbnail: tab.favIconUrl
        });
      });
    }
  },
  { urls: ["<all_urls>"] }
);

// Connect on startup
connectToNativeApp();

// Ping to keep connection alive
setInterval(() => {
  if (ws && isConnected) {
    try {
      ws.send(JSON.stringify({ type: 'ping' }));
    } catch (error) {
      console.error('Ping failed:', error);
    }
  }
}, 30000);
