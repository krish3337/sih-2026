chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyze-standards",
    title: "Analyze with Indian Standards AI",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyze-standards" && info.selectionText) {
    // Save selected text to local storage
    chrome.storage.local.set({ selectedSpecificationText: info.selectionText }, () => {
      // In Manifest V3, we cannot automatically open the popup from a background script.
      // So we will just show a badge or leave it to the user to open the popup.
      chrome.action.setBadgeText({ text: "1" });
      chrome.action.setBadgeBackgroundColor({ color: "#16a34a" }); // Emerald 600
    });
  }
});

// Clear badge when popup is opened
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "clearBadge") {
    chrome.action.setBadgeText({ text: "" });
  }
});
