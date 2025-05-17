document.addEventListener('DOMContentLoaded', () => {
    const statusDiv = document.getElementById('status');
    
    // Оновлюємо статус розширення
    function updateStatus(isActive) {
        statusDiv.textContent = isActive ? 'Extension is active' : 'Extension is inactive';
        statusDiv.className = `status ${isActive ? 'active' : 'inactive'}`;
    }

    // Перевіряємо, чи відкрита сторінка YouTube
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        const currentTab = tabs[0];
        if (currentTab.url.includes('youtube.com')) {
            updateStatus(true);
        } else {
            updateStatus(false);
        }
    });
});