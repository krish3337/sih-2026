// Listen for messages from the popup to get the current selected text
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getSelectedText") {
    const selectedText = window.getSelection().toString().trim();
    sendResponse({ text: selectedText });
  }
  return true; // Keep the message channel open for async response if needed
});
