const chatContainer = document.getElementById("chat");
const userInput = document.getElementById("user-input");
const sendButton = document.getElementById("send-button");
const typingIndicator = document.getElementById("typing-indicator");
const emptyState = chatContainer.querySelector('.empty-state');

userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
    sendButton.disabled = !this.value.trim();
});

userInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendButton.disabled = true;

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    if (emptyState) emptyState.style.display = 'none';

    addUserMessage(message);

    userInput.value = "";
    userInput.style.height = 'auto';
    sendButton.disabled = true;

    scrollToBottom();
    showTypingIndicator();

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        hideTypingIndicator();

        addBotMessage(data.reply);

        if (data.suggestions) {
            addSuggestions(data.suggestions);
        }

    } catch (error) {
        hideTypingIndicator();
        addBotMessage("⚠️ Sorry, I encountered an error. Please try again.");
    }
}

function sendQuickReply(text) {
    userInput.value = text;
    sendMessage();
}

function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'message user-message';
    div.innerHTML = `<div class="message-bubble">${escapeHtml(text)}</div>`;
    chatContainer.appendChild(div);
}

function addBotMessage(text) {
    const div = document.createElement('div');
    div.className = 'message bot-message';
    div.innerHTML = `<div class="message-bubble">${escapeHtml(text)}</div>`;
    chatContainer.appendChild(div);
    scrollToBottom();
}

function addSuggestions(suggestions) {
    const buttonWrap = document.createElement('div');
    buttonWrap.className = 'suggestion-buttons';
    buttonWrap.innerHTML = suggestions.map(s =>
        `<button onclick="sendQuickReply('${s}')">${s}</button>`
    ).join(" ");
    chatContainer.appendChild(buttonWrap);
    scrollToBottom();
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Bot initiates conversation when page loads
window.addEventListener('load', async () => {
    userInput.focus();

    try {
        const res = await fetch("/initial");
        const data = await res.json();

        const h3 = document.querySelector(".empty-state h3");
        const p = document.querySelector(".empty-state p");
        const emptyState = document.querySelector(".empty-state");

        // Typing effect on h3 and p
        await typeWriter(h3, "🤖 " + data.reply.split("\n")[0], 25);
        await typeWriter(p, data.reply.split("\n").slice(1).join(" "), 10);

        if (data.suggestions) {
            const suggestionWrap = document.createElement("div");
            suggestionWrap.className = "suggestion-buttons";

            data.suggestions.forEach(item => {
                const btn = document.createElement("button");
                btn.textContent = item;
                btn.onclick = () => sendQuickReply(item);
                suggestionWrap.appendChild(btn);
            });

            emptyState.appendChild(suggestionWrap);
        }

    } catch (err) {
        console.error("Failed to fetch initial greeting:", err);
    }
});

// Typing animation
async function typeWriter(el, text, speed = 20) {
    el.textContent = "";
    for (let i = 0; i < text.length; i++) {
        el.textContent += text.charAt(i);
        await new Promise(r => setTimeout(r, speed));
    }
}
