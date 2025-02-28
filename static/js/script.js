async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (!userInput.trim()) return;

    let userMessage = `<div class="user-message"><b>You:</b> ${userInput.replace(/\n/g, "<br>")}</div>`;
    chatBox.innerHTML += userMessage;

    document.getElementById("user-input").value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput }),
        });

        let data = await response.json();
        let botReply = `<div class="bot-message"><b>Bot:</b> <span class="typing"></span></div>`;
        chatBox.innerHTML += botReply;
        chatBox.scrollTop = chatBox.scrollHeight;
        let typingElements = document.querySelectorAll(".typing");
        let lastTypingElement = typingElements.length > 0 ? typingElements[typingElements.length - 1] : null;
        await typeText(lastTypingElement, data.reply);
    } catch (error) {
        console.error("Error:", error);
    }
}

async function typeText(element, text) {
    for (let i = 0; i < text.length; i++) {
        element.innerHTML += text[i];
        await new Promise(resolve => setTimeout(resolve, 25)); // Typing speed
    }
}

async function clearChat() {
    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = "";

    try {
        await fetch("/clear_chat", { method: "POST" });
    } catch (error) {
        console.error("Error clearing chat:", error);
    }
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        if (event.shiftKey) {
            // Shift + Enter = New line
            event.preventDefault();
            let input = document.getElementById("user-input");
            input.value += "\n";
        } else {
            // Enter = Send message
            event.preventDefault();
            sendMessage();
        }
    }
}
