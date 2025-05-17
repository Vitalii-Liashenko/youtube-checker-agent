class YouTubeController {
    constructor() {
        this.backendUrl = 'http://localhost:8080';
        this.observer = null;
        this.cache = new Map(); // Cache for storing results
        this.currentVideoId = null;
        this.userInteracted = false; // Track if user has interacted with the page
        this.setupObserver();
        this.setupUserInteractionTracking();
    }

    setupUserInteractionTracking() {
        // Track mouse clicks
        document.addEventListener('click', () => {
            this.userInteracted = true;
            console.log('[YouTube Checker] User interaction detected');
        });

        // Track keyboard interactions
        document.addEventListener('keydown', () => {
            this.userInteracted = true;
            console.log('[YouTube Checker] User interaction detected');
        });
    }

    setupObserver() {
        this.observer = new MutationObserver(() => this.checkCurrentVideo());
        this.observer.observe(document.body, { childList: true, subtree: true });
    }

    async checkCurrentVideo() {
        const videoId = this.getVideoId();
        if (videoId && videoId !== this.currentVideoId) {
            this.currentVideoId = videoId;
            this.userInteracted = false; // Reset user interaction when video changes
            this.removeWarning();
            await this.checkVideoWithBackend(videoId);
        }
    }

    getVideoId() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('v');
    }

    async checkVideoWithBackend(videoId) {
        try {
            // Check cache
            if (this.cache.has(videoId)) {
                console.log(`[YouTube Checker] Using cached result for video: ${videoId}`);
                const cachedData = this.cache.get(videoId);
                if (cachedData.isRussian) {
                    this.showWarning();
                    // Skip to next video only if user hasn't interacted
                    if (!this.userInteracted) {
                        setTimeout(() => {
                            this.playNextVideo();
                        }, 1000);
                    } else {
                        console.log('[YouTube Checker] Skipping auto-transition due to user interaction');
                    }
                }
                return;
            }

            console.log(`[YouTube Checker] Checking video: ${videoId}`);
            const response = await fetch(`${this.backendUrl}/info/videos/${videoId}`, {
                method: 'GET',
                mode: 'cors',
                headers: {
                    'Accept': 'application/json',
                    'Origin': window.location.origin
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log(`[YouTube Checker] Response:`, data);

            // Store result in cache
            this.cache.set(videoId, data);

            if (data.isRussian) {
                this.showWarning();
                // Skip to next video only if user hasn't interacted
                if (!this.userInteracted) {
                    setTimeout(() => {
                        this.playNextVideo();
                    }, 1000);
                } else {
                    console.log('[YouTube Checker] Skipping auto-transition due to user interaction');
                }
            }
        } catch (error) {
            console.error('[YouTube Checker] Error:', error);
        }
    }

    showWarning() {
        // Check if warning already exists
        if (document.querySelector('.youtube-checker-warning')) {
            return;
        }

        const warningDiv = document.createElement('div');
        warningDiv.className = 'youtube-checker-warning';
        warningDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background-color: #ff0000;
            color: white;
            text-align: center;
            padding: 10px;
            z-index: 9999;
            font-weight: bold;
        `;
        warningDiv.textContent = '⚠️ Warning! This video is from a Russian channel';

        // Create close button
        const closeButton = document.createElement('button');
        closeButton.textContent = '×';
        closeButton.style.cssText = `
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 0 10px;
            line-height: 1;
        `;
        closeButton.onmouseover = () => {
            closeButton.style.opacity = '0.8';
        };
        closeButton.onmouseout = () => {
            closeButton.style.opacity = '1';
        };
        closeButton.onclick = () => {
            warningDiv.remove();
        };

        warningDiv.appendChild(closeButton);
        document.body.appendChild(warningDiv);
    }

    removeWarning() {
        const existingWarning = document.querySelector('.youtube-checker-warning');
        if (existingWarning) {
            existingWarning.remove();
        }
    }

    playNextVideo() {
        const nextButton = document.querySelector('.ytp-next-button');
        if (nextButton) {
            console.log('[YouTube Checker] Skipping to next video');
            nextButton.click();
        }
    }
}

// Initialize controller only once when page loads
window.addEventListener('load', () => {
    new YouTubeController();
});