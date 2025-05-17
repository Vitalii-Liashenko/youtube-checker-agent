chrome.runtime.onInstalled.addListener(() => {
    console.log('YouTube AutoPlay Controller installed');
});

// Слухаємо повідомлення від content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === 'VIDEO_CHECKED') {
        // Можна додати додаткову логіку тут
        console.log('Video checked:', request.videoId);
    }
});