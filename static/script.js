// Dark/Light Mode Toggle
document.addEventListener('DOMContentLoaded', function() {
    const modeToggle = document.getElementById('modeToggle');
    const body = document.body;
    
    // Check for saved mode preference or use preferred color scheme
    const savedMode = localStorage.getItem('mode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode === 'dark' || (!savedMode && prefersDark)) {
        body.classList.add('dark-mode');
        if (modeToggle) modeToggle.textContent = '☀️ Light Mode';
    }
    
    // Toggle mode
    if (modeToggle) {
        modeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-mode');
            const isDarkMode = body.classList.contains('dark-mode');
            localStorage.setItem('mode', isDarkMode ? 'dark' : 'light');
            modeToggle.textContent = isDarkMode ? '☀️ Light Mode' : '🌙 Dark Mode';
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
            
            if (msg.sender === currentUser) {
                messageDiv.classList.add('sent');
            } else {
                messageDiv.classList.add('received');
            }
            
            const infoDiv = document.createElement('div');
            infoDiv.classList.add('message-info');
            infoDiv.textContent = `${msg.display_name} • ${msg.timestamp}`;
            
            const textDiv = document.createElement('div');
            textDiv.textContent = msg.message;
            
            messageDiv.appendChild(infoDiv);
            messageDiv.appendChild(textDiv);
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
                body: JSON.stringify({ message: message })
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
