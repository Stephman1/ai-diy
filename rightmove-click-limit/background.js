// Initialize click count and reset time if not set
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ clickCount: 50, lastReset: Date.now(), clickLimitReached: false });
});

// Reset click count every 24 hours
function resetClicksIfNeeded() {
  chrome.storage.local.get("lastReset", (data) => {
    const now = Date.now();
    const oneDay = 24 * 60 * 60 * 1000;

    if (now - data.lastReset >= oneDay) {
      console.log("24 hours passed, resetting click count.");
      chrome.storage.local.set({ clickCount: 50, lastReset: now, clickLimitReached: false });
    }
  });
}

// Listen for messages from content.js to update click count
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "decrementClick") {
    chrome.storage.local.get(["clickCount", "clickLimitReached"], (data) => {
      let clickCount = data.clickCount || 50;
      let clickLimitReached = data.clickLimitReached || false;

      if (clickCount > 0) {
        clickCount = Math.max(0, clickCount - 1);
      }

      // Set click limit reached flag if count hits zero
      clickLimitReached = clickCount <= 0;

      chrome.storage.local.set({ clickCount, clickLimitReached }, () => {
        sendResponse({ clickCount });
      });
    });
    return true;  // Keep sendResponse active for async response
  }
});

// Check every hour if reset is needed
setInterval(resetClicksIfNeeded, 1000 * 60 * 60);
