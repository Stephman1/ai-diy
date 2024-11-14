// Update the click count in the popup
function updatePopup() {
  chrome.storage.local.get("clickCount", (data) => {
    document.getElementById("clickCount").innerText = data.clickCount;
  });
}

// Reset click count to 50
document.getElementById("resetButton").addEventListener("click", () => {
  chrome.storage.local.set({ clickCount: 50 });
  updatePopup();
});

updatePopup();
