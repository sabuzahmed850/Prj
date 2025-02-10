const express = require("express");
const http = require("http");
const socketIo = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static(__dirname));

const responses = {
    "hello": "Hi there! How can I assist you?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "what is your name": "I'm your chatbot assistant.",
    "bye": "Goodbye! Have a nice day!",
    "default": "Sorry, I didn't understand that. Can you rephrase?"
};

io.on("connection", (socket) => {
    console.log("User connected");

    socket.on("message", (msg) => {
        console.log("User:", msg);
        const response = responses[msg.toLowerCase()] || responses["default"];

        setTimeout(() => {
            console.log("Bot:", response);
            socket.emit("bot-message", response);
        }, 1000);
    });

    socket.on("disconnect", () => {
        console.log("User disconnected");
    });
});

const PORT = process.env.PORT || 5000; // Change port from 3000 to 4000
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
