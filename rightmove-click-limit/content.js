console.log("Content script loaded.");

function checkClickCount() {
  chrome.runtime.sendMessage({ action: "decrementClick" }, (response) => {
    const clickCount = response.clickCount;
    console.log(`Click registered. Remaining clicks: ${clickCount}`);
    if (clickCount <= 0) {
      showWarningOverlay();
    }
  });
}

function showWarningOverlay() {
  if (!document.getElementById("warningOverlay")) {
    const overlay = document.createElement("div");
    overlay.id = "warningOverlay";
    overlay.style.position = "fixed";
    overlay.style.top = "0";
    overlay.style.left = "0";
    overlay.style.width = "100%";
    overlay.style.height = "100%";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.8)";
    overlay.style.color = "white";
    overlay.style.zIndex = "1000";
    overlay.style.display = "flex";
    overlay.style.flexDirection = "column";
    overlay.style.alignItems = "center";
    overlay.style.justifyContent = "center";
    
    overlay.innerHTML = `
      <div style="text-align: center;">
        <img src="${chrome.runtime.getURL("warning.gif")}" alt="Warning" />
        <p>You have reached your 50-click limit.</p>
        <button id="continueButton">Continue Anyway</button>
      </div>
    `;
    
    document.body.appendChild(overlay);

    document.getElementById("continueButton").addEventListener("click", () => {
      overlay.remove();
    });
  }
}

// Track clicks on the page
document.addEventListener("click", () => {
  checkClickCount();
});
