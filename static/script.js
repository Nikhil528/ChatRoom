document.addEventListener('DOMContentLoaded', function() {
    // Dark/Light Mode Toggle
    const modeToggle = document.getElementById('modeToggle');
    const body = document.body;
    
    // Initialize mode
    const savedMode = localStorage.getItem('mode');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode === 'dark' || (!savedMode && prefersDark)) {
        body.classList.add('dark-mode');
        if (modeToggle) modeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    
    // Toggle mode
    if (modeToggle) {
        modeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-mode');
            const isDarkMode = body.classList.contains('dark-mode');
            localStorage.setItem('mode', isDarkMode ? 'dark' : 'light');
            modeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
    }
    
    // Chat functionality
    if (document.getElementById('chatMessages')) {
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        
        // Load messages
        function loadMessages() {
            fetch('/get_messages')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        displayMessages(data.messages);
                    }
                })
                .catch(error => {
                    console.error('Error loading messages:', error);
                });
        }
        
        // Display messages
        function displayMessages(messages) {
            chatMessages.innerHTML = '';
            
            messages.forEach(msg => {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                
                if (msg.sender === currentUser.username) {
                    messageDiv.classList.add('sent');
                    messageDiv.style.backgroundColor = msg.color;
                } else {
                    messageDiv.classList.add('received');
                    messageDiv.style.backgroundColor = msg.opposite_color;
                    messageDiv.style.color = 'var(--text-color)';
                }
                
                messageDiv.innerHTML = `
                    <div class="message-info">
                        <img src="${msg.avatar}" class="message-avatar">
                        <span>${msg.display_name}</span>
                        <span>• ${msg.timestamp}</span>
                    </div>
                    <div class="message-content">${msg.message}</div>
                `;
                
                chatMessages.appendChild(messageDiv);
            });
            
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        // Send message
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
                .then(response => response.json())
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
        
        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Initial load and refresh every 2 seconds
        loadMessages();
        setInterval(loadMessages, 2000);
    }
});
