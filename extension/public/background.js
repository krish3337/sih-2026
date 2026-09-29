chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "analyze-standards",
    title: "Analyze with Indian Standards AI",
    contexts: ["selection"]
  });

  // Enable opening the side panel by clicking the extension icon
  if (chrome.sidePanel) {
    chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch((error) => console.error(error));
  }
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "analyze-standards" && info.selectionText) {
    // Save selected text to local storage
    chrome.storage.local.set({ selectedSpecificationText: info.selectionText }, () => {
      // Open the side panel automatically!
      if (chrome.sidePanel && tab && tab.windowId) {
        chrome.sidePanel.open({ windowId: tab.windowId }).catch(console.error);
      } else {
        chrome.action.setBadgeText({ text: "1" });
        chrome.action.setBadgeBackgroundColor({ color: "#16a34a" });
      }
    });
  }
});

// Clear badge when popup is opened
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "clearBadge") {
    chrome.action.setBadgeText({ text: "" });
  }
});


