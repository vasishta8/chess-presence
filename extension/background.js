async function updateDiscord(tabId) {
    try {
        const tab = await chrome.tabs.get(tabId);

        if (!tab.url || tab.url.startsWith('chrome://') || tab.url.startsWith('edge://') || tab.url.startsWith('brave://')) {
            console.log("Skipping internal or empty URL");
            return;
        }

        console.log("Sending update for:", tab.title);

        const response = await fetch('http://localhost:5000/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: tab.title,
                url: tab.url
            })
        });

        if (response.ok) {
            console.log('Successfully updated Discord');
        }
    } catch (error) {
        console.error('Error in bridge:', error);
    }
}

chrome.tabs.onActivated.addListener((activeInfo) => {
    updateDiscord(activeInfo.tabId);
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete') {
        updateDiscord(tabId);
    }
});