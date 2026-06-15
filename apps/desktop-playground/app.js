const contactData = {
  robert: {
    name: "Robert",
    status: "Verified contact",
    safety: "123-456-789-012",
    messages: [
      { direction: "received", body: "Hello from the encrypted local app store." },
      { direction: "sent", body: "Testing the LeftLevel playground UI." }
    ]
  },
  maya: {
    name: "Maya",
    status: "New contact",
    safety: "789-222-451-009",
    messages: [
      { direction: "received", body: "New contact waiting for verification." }
    ]
  },
  sam: {
    name: "Sam",
    status: "Safety number changed",
    safety: "CHANGED — verify before sensitive messages",
    messages: [
      { direction: "received", body: "This contact needs re-verification." }
    ]
  }
};

let activeContact = "robert";

function renderContact(key) {
  activeContact = key;
  const data = contactData[key];
  document.querySelector(".eyebrow").textContent = data.status;
  document.querySelector("#contactName").textContent = data.name;
  document.querySelector("#safetyCode").textContent = `Safety: ${data.safety}`;
  document.querySelectorAll(".contact").forEach((button) => {
    button.classList.toggle("active", button.dataset.contact === key);
  });
  const messages = document.querySelector("#messages");
  messages.innerHTML = "";
  data.messages.forEach((message) => {
    const item = document.createElement("div");
    item.className = `message ${message.direction}`;
    item.textContent = message.body;
    messages.appendChild(item);
  });
}

document.querySelectorAll(".contact").forEach((button) => {
  button.addEventListener("click", () => renderContact(button.dataset.contact));
});

document.querySelector("#sendButton").addEventListener("click", () => {
  const input = document.querySelector("#messageInput");
  const body = input.value.trim();
  if (!body) return;
  contactData[activeContact].messages.push({ direction: "sent", body });
  input.value = "";
  renderContact(activeContact);
});
