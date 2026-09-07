const launcher = document.getElementById("chat-launcher");
const panel = document.getElementById("chat-panel");
const closeBtn = document.getElementById("chat-close");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const messages = document.getElementById("chat-messages");

function addMessage(text, kind = "bot") {
  const bubble = document.createElement("div");
  bubble.className = `msg ${kind}`;
  bubble.textContent = text;
  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
  return bubble;
}

function openChat() {
  panel.classList.remove("hidden");
  launcher.classList.add("hidden");
  launcher.setAttribute("aria-expanded", "true");

  if (!messages.children.length) {
    addMessage("Hi, welcome to Bella Vista. Ask us about hours, menu items, or reservations.");
  }

  input.focus();
}

function closeChat() {
  panel.classList.add("hidden");
  launcher.classList.remove("hidden");
  launcher.setAttribute("aria-expanded", "false");
  launcher.focus();
}

launcher.addEventListener("click", openChat);
closeBtn.addEventListener("click", closeChat);

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const text = input.value.trim();
  if (!text) return;

  addMessage(text, "user");
  input.value = "";

  const typing = addMessage("Thinking...", "bot typing");
  setTimeout(() => {
    typing.remove();
    addMessage("Thanks. We’ll get back to you shortly. For bookings, please call the restaurant directly.");
  }, 700);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !panel.classList.contains("hidden")) {
    closeChat();
  }
});
