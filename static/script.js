const room_id = "{{ room_id }}";  // From Flask template
const user_id = Math.random().toString(36).substr(2, 9); // Random user ID

const socket = io();
const videoGrid = document.getElementById('video-grid');
const messagesDiv = document.getElementById('messages');
const messageInput = document.getElementById('message-input');

let peers = {};
let localStream;

// Initialize WebRTC
async function init() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        addVideoStream(user_id, localStream);
        
        socket.emit('join', { room_id, user_id });
        
        socket.on('existing_users', users => {
            users.users.forEach(user => {
                if (user !== user_id) createPeer(user);
            });
        });

        socket.on('user_joined', data => {
            createPeer(data.user_id);
        });

        socket.on('user_left', data => {
            if (peers[data.user_id]) {
                peers[data.user_id].close();
                delete peers[data.user_id];
            }
        });

        socket.on('signal', data => {
            if (data.target_user_id === user_id) {
                peers[data.user_id].signal(data.signal);
            }
        });

        socket.on('chat_message', data => {
            addMessage(`${data.user_id}: ${data.message}`);
        });
    } catch (err) {
        console.error("Media access error:", err);
    }
}

function createPeer(targetUserId) {
    const peer = new SimplePeer({ initiator: true, stream: localStream });
    
    peer.on('signal', signal => {
        socket.emit('signal', {
            target_user_id: targetUserId,
            user_id,
            signal
        });
    });

    peer.on('stream', stream => {
        addVideoStream(targetUserId, stream);
    });

    peers[targetUserId] = peer;
}

function addVideoStream(userId, stream) {
    const video = document.createElement('video');
    video.srcObject = stream;
    video.autoplay = true;
    video.className = 'video-element';
    video.setAttribute('data-user-id', userId);
    videoGrid.appendChild(video);
}

function sendMessage() {
    const message = messageInput.value;
    if (message.trim() === '') return;
    
    socket.emit('chat_message', { room_id, user_id, message });
    addMessage(`You: ${message}`);
    messageInput.value = '';
}

function addMessage(message) {
    const messageEl = document.createElement('div');
    messageEl.textContent = message;
    messagesDiv.appendChild(messageEl);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Start on load
init();
