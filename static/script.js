document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const chatForm = document.getElementById("chat-form");
    const messageInput = document.getElementById("message-input");
    const replyBox = document.getElementById("reply-to");
    const replyText = document.getElementById("reply-text");

    let replyToMessage = null;

    if (chatForm) {
        chatForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (!message) return;

            const payload = { message };
            if (replyToMessage) {
                payload.reply_to = replyToMessage;
            }

            await fetch('/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            messageInput.value = "";
            cancelReply();
            loadMessages();
        });

        window.cancelReply = () => {
            replyToMessage = null;
            replyBox.classList.add("hidden");
            replyText.textContent = "";
        };

        async function loadMessages() {
            const res = await fetch('/get_messages');
            const data = await res.json();
            chatBox.innerHTML = "";

            data.forEach(msg => {
                const wrapper = document.createElement("div");
                wrapper.className = "flex items-start space-x-2";
                if (msg.sender === username) {
                    wrapper.classList.add("flex-row-reverse", "justify-end");
                }

                const avatar = document.createElement("div");
                avatar.className = "text-2xl";
                avatar.textContent = msg.sender === "user1" ? "👤" : "🧑‍💼";

                const bubble = document.createElement("div");
                bubble.className = "p-3 rounded-xl max-w-[75%] break-words";
                if (msg.sender === username) {
                    bubble.classList.add("bg-blue-500", "text-white", "text-right");
                } else {
                    bubble.classList.add("bg-gray-200", "dark:bg-gray-700", "text-gray-800", "dark:text-white", "text-left");
                }

                if (msg.reply_to) {
                    const reply = document.createElement("div");
                    reply.className = "text-sm italic bg-gray-100 dark:bg-gray-800 p-2 rounded mb-2";
                    reply.textContent = `${msg.reply_to.sender}: ${msg.reply_to.message}`;
                    bubble.appendChild(reply);
                }

                const msgText = document.createElement("div");
                msgText.textContent = msg.message;
                bubble.appendChild(msgText);

                bubble.addEventListener("click", () => {
                    replyToMessage = {
                        sender: msg.sender,
                        message: msg.message
                    };
                    replyText.textContent = `Replying to ${msg.sender}: ${msg.message}`;
                    replyBox.classList.remove("hidden");
                });

                wrapper.appendChild(avatar);
                wrapper.appendChild(bubble);
                chatBox.appendChild(wrapper);
            });

            chatBox.scrollTop = chatBox.scrollHeight;
        }

        setInterval(loadMessages, 1000);
        loadMessages();
    }

    // Theme toggle
   
