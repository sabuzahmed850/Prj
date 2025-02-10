document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const messageInput = document.getElementById("message");
    const sendButton = document.getElementById("send");

    const socket = io("http://localhost:5000");

//const socket = io("http://localhost:3000");

    sendButton.addEventListener("click", () => {
        const message = messageInput.value.trim();
        if (message) {
            appendMessage("You", message);
            console.log("Sending message:", message); // Debugging
            socket.emit("message", message);
            messageInput.value = "";
        }
    });

    socket.on("bot-message", (message) => {
        console.log("Received bot message:", message); // Debugging
        appendMessage("Bot", message);
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement("div");
        messageElement.textContent = `${sender}: ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
