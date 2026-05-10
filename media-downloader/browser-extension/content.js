// Content script to detect media elements
console.log('Media Downloader Helper: Content script loaded');

// Detect video and audio elements
function detectMediaElements() {
  const mediaElements = document.querySelectorAll('video, audio');
  
  mediaElements.forEach(element => {
    // Skip if already processed
    if (element.dataset.mediaDownloaderProcessed) {
      return;
    }
    
    element.dataset.mediaDownloaderProcessed = 'true';
    
    // Listen for play event
    element.addEventListener('play', () => {
      const mediaInfo = {
        type: 'media_detected',
        url: element.currentSrc || element.src,
        title: document.title || 'Unknown',
        mediaType: element.tagName.toLowerCase(),
        pageUrl: window.location.href,
        thumbnail: extractThumbnail(element)
      };
      
      console.log('Media playback detected:', mediaInfo);
      
      // Send to background script
      chrome.runtime.sendMessage(mediaInfo, (response) => {
        if (chrome.runtime.lastError) {
          console.error('Error sending message:', chrome.runtime.lastError);
        }
      });
    });
  });
}

// Extract thumbnail from video element
function extractThumbnail(element) {
  if (element.tagName === 'VIDEO') {
    return element.poster || null;
  }
  return null;
}

// Detect YouTube videos
function detectYouTubeVideo() {
  if (window.location.hostname.includes('youtube.com')) {
    const videoId = new URLSearchParams(window.location.search).get('v');
    if (videoId) {
      const url = window.location.href;
      const title = document.querySelector('h1.title')?.textContent || 
                   document.querySelector('meta[name="title"]')?.content ||
                   document.title;
      
      chrome.runtime.sendMessage({
        type: 'media_detected',
        url: url,
        title: title,
        mediaType: 'video',
        pageUrl: window.location.href,
        thumbnail: `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`
      });
    }
  }
}

// Detect Vimeo videos
function detectVimeoVideo() {
  if (window.location.hostname.includes('vimeo.com')) {
    const videoMatch = window.location.pathname.match(/\/(\d+)/);
    if (videoMatch) {
      const url = window.location.href;
      const title = document.querySelector('meta[property="og:title"]')?.content ||
                   document.title;
      
      chrome.runtime.sendMessage({
        type: 'media_detected',
        url: url,
        title: title,
        mediaType: 'video',
        pageUrl: window.location.href,
        thumbnail: document.querySelector('meta[property="og:image"]')?.content
      });
    }
  }
}

// Run detection on page load
detectMediaElements();
detectYouTubeVideo();
detectVimeoVideo();

// Watch for dynamically added media elements
const observer = new MutationObserver(() => {
  detectMediaElements();
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});

// Listen for navigation changes (SPAs)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    detectYouTubeVideo();
    detectVimeoVideo();
  }
}).observe(document, { subtree: true, childList: true });
