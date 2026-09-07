const launcher = document.getElementById("chat-launcher");
const panel = document.getElementById("chat-panel");
const closeBtn = document.getElementById("chat-close");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const messagesEl = document.getElementById("chat-messages");

let history = [];

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function openChat() {
  panel.classList.remove("hidden");
  launcher.classList.add("hidden");
  if (history.length === 0) {
    addMessage("bot", "Ciao! I'm the virtual host for Bella Vista. Ask me about hours, the menu, reservations, or allergens.");
  }
  input.focus();
}

function closeChat() {
  panel.classList.add("hidden");
  launcher.classList.remove("hidden");
}

launcher.addEventListener("click", openChat);
closeBtn.addEventListener("click", closeChat);

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;

  addMessage("user", text);
  history.push({ role: "user", content: text });
  input.value = "";

  const typingEl = addMessage("bot typing", "Typing…");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    const data = await res.json();

    typingEl.remove();

    if (data.error) {
      addMessage("bot", "Sorry, something went wrong on our end. Please call us at (555) 010-2938.");
      return;
    }

    addMessage("bot", data.reply);
    history.push({ role: "assistant", content: data.reply });
  } catch (err) {
    typingEl.remove();
    addMessage("bot", "I'm having trouble connecting right now — please try again in a moment.");
  }
});
