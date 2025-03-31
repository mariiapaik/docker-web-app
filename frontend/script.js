const API_URL = window.env?.API_URL;

async function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();

    if (!text) return alert("Enter a message!");

    const response = await fetch(`${API_URL}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    if (response.ok) {
        input.value = "";
        loadMessages();
    } else {
        alert("Failed to send message");
    }
}

async function loadMessages() {
    try {
        const response = await fetch(`${API_URL}/messages`);
        const messages = await response.json();

        const messagesList = document.getElementById("messagesList");
        messagesList.innerHTML = "";

        messages.forEach(msg => {
            const li = document.createElement("li");
            li.textContent = msg.text;
            messagesList.appendChild(li);
        });
    } catch (error) {
        console.error("Failed to load messages:", error);
    }
}

document.addEventListener("DOMContentLoaded", loadMessages);
