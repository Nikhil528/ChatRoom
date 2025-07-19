document.addEventListener('DOMContentLoaded', function() {
    // Theme toggle functionality
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }
    
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        
        if (document.body.classList.contains('dark-theme')) {
            localStorage.setItem('theme', 'dark');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        } else {
            localStorage.setItem('theme', 'light');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
        }
    });
    
    // Chat functionality
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    
    // Focus message input on load
    messageInput.focus();
    
    // Send message on button click
    sendButton.addEventListener('click', sendMessage);
    
    // Send message on Enter key
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Function to send message
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            // Send message to server
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Clear input
                    messageInput.value = '';
                    // Fetch updated messages
                    fetchMessages();
                }
            });
        }
    }
    
    // Function to fetch messages from server
    function fetchMessages() {
        fetch('/get_messages')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                displayMessages(data.messages);
            }
        });
    }
    
    // Function to display messages
    function displayMessages(messages) {
        // Clear chat messages container
        chatMessages.innerHTML = '';
        
        // Get current username from the page
        const username = document.querySelector('.header-left p strong').textContent;
        
        // Add each message to the chat
        messages.forEach(msg => {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            
            if (msg.sender === username) {
                messageElement.classList.add('message-self');
            } else {
                messageElement.classList.add('message-other');
            }
            
            messageElement.innerHTML = `
                <div class="message-sender">${msg.sender}</div>
                <div class="message-content">${msg.message}</div>
                <div class="message-time">${msg.timestamp}</div>
            `;
            
            chatMessages.appendChild(messageElement);
        });
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Fetch messages initially and then every 2 seconds
    fetchMessages();
    setInterval(fetchMessages, 2000);
});
