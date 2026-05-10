// Popup script
document.addEventListener('DOMContentLoaded', () => {
  const statusDiv = document.getElementById('status');
  const testButton = document.getElementById('testButton');
  
  // Check connection status
  function checkConnection() {
    chrome.runtime.sendMessage({ type: 'check_connection' }, (response) => {
      if (chrome.runtime.lastError) {
        updateStatus(false);
        return;
      }
      
      updateStatus(response.connected);
    });
  }
  
  // Update UI based on connection status
  function updateStatus(connected) {
    if (connected) {
      statusDiv.textContent = '✓ Connected to Media Downloader';
      statusDiv.className = 'status connected';
      testButton.disabled = false;
    } else {
      statusDiv.textContent = '✗ Not connected - Start the app';
      statusDiv.className = 'status disconnected';
      testButton.disabled = true;
    }
  }
  
  // Test button click
  testButton.addEventListener('click', () => {
    chrome.runtime.sendMessage({
      type: 'media_detected',
      url: 'https://example.com/test.mp4',
      title: 'Test Video',
      mediaType: 'video',
      pageUrl: 'https://example.com',
      thumbnail: null
    }, (response) => {
      if (response && response.success) {
        alert('Test notification sent! Check the Media Downloader app.');
      } else {
        alert('Failed to send test notification.');
      }
    });
  });
  
  // Initial check
  checkConnection();
  
  // Check periodically
  setInterval(checkConnection, 2000);
});
