// Initialize click count and reset time if not set
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ clickCount: 50, lastReset: Date.now() });
});

// Reset click count every 24 hours
function resetClicksIfNeeded() {
  chrome.storage.local.get("lastReset", (data) => {
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;

    if (now - data.lastReset >= oneDay) {
      console.log("24 hours passed, resetting click count.");
      chrome.storage.local.set({ clickCount: 50, lastReset: now });
    }
  });
}

// Listen for messages from content.js to update click count
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "decrementClick") {
    chrome.storage.local.get("clickCount", (data) => {
      let clickCount = data.clickCount || 50;
      clickCount = Math.max(0, clickCount - 1);
      chrome.storage.local.set({ clickCount }, () => {
        sendResponse({ clickCount });
      });
    });
    return true;  // Keep sendResponse active for async response
  }
});

// Check every hour if reset is needed
setInterval(resetClicksIfNeeded, 1000 * 60 * 60);
