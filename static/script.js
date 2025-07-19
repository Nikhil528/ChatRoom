// Initialize socket connection
let socket;

function initChat(currentUser) {
    // DOM Elements
    const themeToggle = document.getElementById('themeToggle');
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const connectionStatus = document.getElementById('connectionStatus');

    // Theme Toggle
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        const icon = themeToggle.querySelector('i');
        if (document.body.classList.contains('dark-mode')) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    });

    // Connect to Socket.IO server
    socket = io();

    // Socket.IO event handlers
    socket.on('connect', () => {
        console.log('Connected to server');
        connectionStatus.textContent = 'Online';
        connectionStatus.style.color = '#00b894';
        
        // Join user-specific room
        socket.emit('join', currentUser.username);
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        connectionStatus.textContent = 'Offline';
        connectionStatus.style.color = '#ff7675';
    });

    socket.on('receive_message', (data) => {
        addMessage(data.text, data.sender, data.timestamp, false);
    });

    socket.on('chat_history', (history) => {
        history.forEach(msg => {
            const isCurrentUser = msg.sender === currentUser.username;
            addMessage(msg.text, msg.sender, msg.timestamp, isCurrentUser);
        });
    });

    socket.on('user_joined', (username) => {
        if (username !== currentUser.username) {
            addSystemMessage(`${username} is online`);
        }
    });

    socket.on('user_left', (username) => {
        if (username !== currentUser.username) {
            addSystemMessage(`${username} is offline`);
        }
    });

    // Send Message Functionality
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            const now = new Date();
            const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            // Add message locally
            addMessage(message, currentUser.username, timestamp, true);
            
            // Send to server
            socket.emit('send_message', {
                text: message,
                sender: currentUser.username,
                timestamp: timestamp
            });
            
            // Clear input
            messageInput.value = '';
        }
    }

    // Add message to chat UI
    function addMessage(text, sender, timestamp, isCurrentUser) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', isCurrentUser ? 'sent' : 'received');
        
        messageElement.innerHTML = `
            <div>${text}</div>
            <span class="message-time">${timestamp} | ${sender}</span>
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Add system message to chat UI
    function addSystemMessage(text) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'system');
        messageElement.innerHTML = `<div class="text-center">${text}</div>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    logoutBtn.addEventListener('click', () => {
        window.location.href = '/logout';
    });
}
