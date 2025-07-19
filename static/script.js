document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
        
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.className = savedTheme;
            updateThemeButton(savedTheme);
        }
    }

    // Mobile keyboard handling
    handleMobileKeyboard();
    
    // Reply functionality
    setupReplyFeature();
    
    // Swipe to reply
    setupSwipeToReply();
});

function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-mode')) {
        body.className = 'light-mode';
        localStorage.setItem('theme', 'light-mode');
        updateThemeButton('light-mode');
    } else {
        body.className = 'dark-mode';
        localStorage.setItem('theme', 'dark-mode');
        updateThemeButton('dark-mode');
    }
}

function updateThemeButton(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = theme === 'dark-mode' ? 'fas fa-sun' : 'fas fa-moon';
        }
    }
}

function handleMobileKeyboard() {
    if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return; // Not a mobile device
    }

    const messageInput = document.querySelector('.message-form input');
    const chatMessages = document.getElementById('chatMessages');

    if (messageInput && chatMessages) {
        messageInput.addEventListener('focus', () => {
            // Scroll to bottom when input is focused
            setTimeout(() => {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }, 300);
        });

        // Handle window resize (keyboard appearing/disappearing)
        window.addEventListener('resize', () => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }
}

function setupReplyFeature() {
    const chatMessages = document.getElementById('chatMessages');
    const replyIndicator = document.getElementById('replyIndicator');
    const replyName = document.getElementById('replyName');
    const replyText = document.getElementById('replyText');
    const replyTo = document.getElementById('replyTo');
    const cancelReply = document.getElementById('cancelReply');
    
    if (!chatMessages) return;
    
    // Click to reply
    chatMessages.addEventListener('click', function(e) {
        const messageContainer = e.target.closest('.message-container');
        if (!messageContainer || messageContainer.classList.contains('sent')) return;
        
        const id = messageContainer.dataset.id;
        const name = messageContainer.querySelector('.message-content p')?.textContent;
        const text = messageContainer.querySelector('.reply-name')?.textContent || 
                    messageContainer.querySelector('.sender-name')?.textContent;
        
        if (id && name && text) {
            replyTo.value = id;
            replyName.textContent = 'Replying to ' + text;
            replyText.textContent = name;
            replyIndicator.style.display = 'flex';
            
            // Scroll to input
            setTimeout(() => {
                document.querySelector('.message-form input').focus();
            }, 100);
        }
    });
    
    // Cancel reply
    if (cancelReply) {
        cancelReply.addEventListener('click', function() {
            replyTo.value = '';
            replyIndicator.style.display = 'none';
        });
    }
}

function setupSwipeToReply() {
    if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return; // Not a mobile device
    }

    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    let startX, startY, distX, distY;
    let swipeThreshold = 50;
    let timeThreshold = 300;
    let startTime;
    let messageContainer;

    chatMessages.addEventListener('touchstart', function(e) {
        messageContainer = e.target.closest('.message-container');
        if (!messageContainer || messageContainer.classList.contains('sent')) return;
        
        const touch = e.touches[0];
        startX = touch.clientX;
        startY = touch.clientY;
        startTime = new Date().getTime();
        e.preventDefault();
    }, {passive: false});

    chatMessages.addEventListener('touchmove', function(e) {
        if (!messageContainer) return;
        
        const touch = e.touches[0];
        distX = touch.clientX - startX;
        distY = touch.clientY - startY;
        
        // Only horizontal swipe
        if (Math.abs(distX) > Math.abs(distY)) {
            e.preventDefault();
            
            // Limit swipe to left (for received messages)
            if (distX < 0) {
                messageContainer.style.transform = `translateX(${distX}px)`;
            }
        }
    }, {passive: false});

    chatMessages.addEventListener('touchend', function(e) {
        if (!messageContainer) return;
        
        const elapsedTime = new Date().getTime() - startTime;
        
        if (elapsedTime <= timeThreshold && Math.abs(distX) >= swipeThreshold) {
            // Swipe left to reply
            if (distX < 0) {
                const id = messageContainer.dataset.id;
                const name = messageContainer.querySelector('.message-content p')?.textContent;
                const text = messageContainer.querySelector('.reply-name')?.textContent || 
                            messageContainer.querySelector('.sender-name')?.textContent;
                
                if (id && name && text) {
                    document.getElementById('replyTo').value = id;
                    document.getElementById('replyName').textContent = 'Replying to ' + text;
                    document.getElementById('replyText').textContent = name;
                    document.getElementById('replyIndicator').style.display = 'flex';
                    
                    // Scroll to input
                    setTimeout(() => {
                        document.querySelector('.message-form input').focus();
                    }, 100);
                }
            }
        }
        
        // Reset
        messageContainer.style.transform = '';
        messageContainer = null;
        startX = startY = distX = distY = 0;
    });
}
