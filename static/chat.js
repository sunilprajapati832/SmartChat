const socket = io();

const chatWidget = document.getElementById("chat-widget");
const chatToggle = document.getElementById("chat-toggle");
const closeBtn = document.getElementById("close-btn");
const chatHeader = document.getElementById("chat-header");
const typingIndicator = document.getElementById("typing-indicator");
const messages = document.getElementById("messages");
/* --------------------
 ENABLE DRAGGING
--------------------- */
makeDraggable(chatToggle, chatToggle);   // AI circle
makeDraggable(chatHeader, chatWidget);   // Chatbox via header

let firstOpen = true;

/* --------------------
 INITIAL STATE
--------------------- */
chatWidget.style.display = "none";
chatToggle.style.display = "flex";
typingIndicator.style.display = "none";

/* --------------------
 OPEN CHAT
--------------------- */
chatToggle.addEventListener("click", () => {
    chatWidget.style.display = "flex";
    chatToggle.style.display = "none";

    if (firstOpen) {
        showTyping();
        setTimeout(() => {
            hideTyping();
            addBotMessage(
                typeof GREETING_TEXT !== "undefined"
                    ? GREETING_TEXT
                    : "Hi! I’m SmartChat 👋 How can I help you today?"
            );
            firstOpen = false;
        }, 800);
    }
});

/* --------------------
 CLOSE CHAT
--------------------- */
closeBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    chatWidget.style.display = "none";
    chatToggle.style.display = "flex";
});

/* --------------------
 SEND MESSAGE
--------------------- */
function sendMessage() {
    const input = document.getElementById("chat-input");
    const text = input.value.trim();

    if (!text) return;

    addUserMessage(text);

    socket.emit("user_message", {
        message: text
    });

    input.value = "";
}

/* ENTER KEY SUPPORT */
document
    .getElementById("chat-input")
    .addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

/* --------------------
 RECEIVE BOT MESSAGE
--------------------- */
socket.on("bot_reply", (data) => {
    showTyping();
    setTimeout(() => {
        hideTyping();
        addBotMessage(data.message);
    }, 700);
});

/* --------------------
 UI HELPERS
--------------------- */
function addUserMessage(text) {
    const div = document.createElement("div");
    div.className = "message visitor";
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function addBotMessage(text) {
    const div = document.createElement("div");
    div.className = "message bot";
    div.innerText = text;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

function showTyping() {
    typingIndicator.style.display = "block";
}

function hideTyping() {
    typingIndicator.style.display = "none";
}

/* --------------------
 GENERIC DRAG FUNCTION
--------------------- */
function makeDraggable(handle, target) {
    let isDragging = false;
    let offsetX = 0;
    let offsetY = 0;

    handle.addEventListener("mousedown", (e) => {
        isDragging = true;

        offsetX = e.clientX - target.offsetLeft;
        offsetY = e.clientY - target.offsetTop;

        target.style.right = "auto";
        target.style.bottom = "auto";

        handle.style.cursor = "grabbing";
    });

    document.addEventListener("mousemove", (e) => {
        if (!isDragging) return;

        target.style.left = e.clientX - offsetX + "px";
        target.style.top = e.clientY - offsetY + "px";
    });

    document.addEventListener("mouseup", () => {
        if (!isDragging) return;

        isDragging = false;
        handle.style.cursor = "move";
    });
}


/* --------------------
 MAKE CHAT WIDGET DRAGGABLE (HEADER ONLY)
--------------------- */
let isDragging = false;
let offsetX = 0;
let offsetY = 0;

chatHeader.addEventListener("mousedown", (e) => {
    isDragging = true;

    offsetX = e.clientX - chatWidget.offsetLeft;
    offsetY = e.clientY - chatWidget.offsetTop;

    chatHeader.style.cursor = "grabbing";
    console.log("Drag started");
});

document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;

    chatWidget.style.left = e.clientX - offsetX + "px";
    chatWidget.style.top = e.clientY - offsetY + "px";

    chatWidget.style.right = "auto";
    chatWidget.style.bottom = "auto";
});

document.addEventListener("mouseup", () => {
    if (isDragging) console.log("Drag ended");
    isDragging = false;
    chatHeader.style.cursor = "move";
});