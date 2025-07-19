// Dark/Light Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    const modeToggle = document.getElementById('modeToggle');
    const body = document.body;
    
    // Check for saved mode preference or use preferred color scheme
    const savedMode = localStorage.getItem('mode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode === 'dark' || (!savedMode && prefersDark)) {
        body.classList.add('dark-mode');
    }
    
    // Toggle mode
    if (modeToggle) {
        modeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-mode');
            const isDarkMode = body.classList.contains('dark-mode');
            localStorage.setItem('mode', isDarkMode ? 'dark' : 'light');
        });
    }
    
    // Chat functionality
    if (document.getElementById('chatMessages')) {
        setupChat();
    }
});

function setupChat() {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const replyPreview = document.getElementById('replyPreview');
    
    let replyingTo = null;
    let touchStartX = 0;
    let touchEndX = 0;
    
    // Load previous messages
    loadMessages();
    
    // Set up periodic message refresh
    const messageInterval = setInterval(loadMessages, 2000);
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Swipe to reply functionality
    chatMessages.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, false);
    
    chatMessages.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);
    
    function handleSwipe() {
        const messageElement = document.elementFromPoint(touchEndX, window.innerHeight / 2);
        if (messageElement && messageElement.closest('.message')) {
            const message = messageElement.closest('.message');
            const messageId = parseInt(message.dataset.id);
            
            // Check if swipe is significant enough
            if (Math.abs(touchEndX - touchStartX) > 50) {
                if (touchEndX < touchStartX && !message.classList.contains('sent')) {
                    // Swipe left to reply
                    const foundMessage = messages.find(m => m.id === messageId);
                    if (foundMessage && foundMessage.sender !== currentUser.username) {
                        setReplyTo(foundMessage);
                        message.classList.add('swipe-left');
                        setTimeout(() => message.classList.remove('swipe-left'), 300);
                    }
                } else if (touchEndX > touchStartX && replyingTo) {
                    // Swipe right to cancel reply
                    cancelReply();
                    message.classList.add('swipe-right');
                    setTimeout(() => message.classList.remove('swipe-right'), 300);
                }
            }
        }
    }
    
    function setReplyTo(message) {
        replyingTo = message;
        showReplyPreview(message);
    }
    
    function cancelReply() {
        replyingTo = null;
        hideReplyPreview();
    }
    
    function showReplyPreview(message) {
        replyPreview.style.display = 'block';
        replyPreview.innerHTML = `
            <div class="reply-preview-content">
                <div class="reply-preview-text">
                    Replying to ${message.display_name}: ${message.message.substring(0, 30)}${message.message.length > 30 ? '...' : ''}
                </div>
                <button class="reply-preview-cancel" id="cancelReply">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.getElementById('cancelReply').addEventListener('click', cancelReply);
    }
    
    function hideReplyPreview() {
        replyPreview.style.display = 'none';
    }
    
    function loadMessages() {
        fetch('/get_messages')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    displayMessages(data.messages);
                }
            })
            .catch(error => {
                console.error('Error loading messages:', error);
            });
    }
    
    function displayMessages(messages) {
        chatMessages.innerHTML = '';
        
        messages.forEach(msg => {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            messageDiv.dataset.id = msg.id;
            
            if (msg.sender === currentUser.username) {
                messageDiv.classList.add('sent');
                messageDiv.style.backgroundColor = currentUser.color;
            } else {
                messageDiv.classList.add('received');
            }
            
            let replyContent = '';
            if (msg.reply_to) {
                const repliedMsg = messages.find(m => m.id === msg.reply_to);
                if (repliedMsg) {
                    replyContent = `
                        <div class="message-reply">
                            ${repliedMsg.display_name}: ${repliedMsg.message.substring(0, 50)}${repliedMsg.message.length > 50 ? '...' : ''}
                        </div>
                    `;
                }
            }
            
            messageDiv.innerHTML = `
                <div class="message-info">
                    <img src="${msg.avatar}" alt="${msg.display_name}" class="message-avatar">
                    <span class="message-sender">${msg.display_name}</span>
                    <span class="message-time">${msg.timestamp}</span>
                </div>
                ${replyContent}
                <div class="message-content">${msg.message}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
        });
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: message,
                    reply_to: replyingTo ? replyingTo.id : null
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    messageInput.value = '';
                    cancelReply();
                    loadMessages();
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
            });
        }
    }
    
    // Clean up interval when leaving the page
    window.addEventListener('beforeunload', function() {
        clearInterval(messageInterval);
    });
}
