const API_BASE = "http://127.0.0.1:8790";

const fallbackContacts = [
  {
    name: "robert",
    displayName: "Robert",
    trust_state: "verified",
    safety_short_code: "123-456-789-012",
    sent: 1,
    received: 1,
    messages: [
      { direction: "received", body: "Hello from the encrypted local app store." },
      { direction: "sent", body: "Testing the LeftLevel playground UI." }
    ]
  },
  {
    name: "maya",
    displayName: "Maya",
    trust_state: "unverified",
    safety_short_code: "789-222-451-009",
    sent: 0,
    received: 1,
    messages: [{ direction: "received", body: "New contact waiting for verification." }]
  },
  {
    name: "sam",
    displayName: "Sam",
    trust_state: "changed",
    safety_short_code: "verify again",
    sent: 0,
    received: 1,
    messages: [{ direction: "received", body: "This contact needs re-verification." }]
  }
];

let contacts = [];
let activeContact = null;
let apiOnline = false;

function trustLabel(state) {
  return { verified: "OK", unverified: "NEW", changed: "CHANGED" }[state] || "NEW";
}

function statusText(state) {
  return { verified: "Verified contact", unverified: "New contact", changed: "Safety number changed" }[state] || "New contact";
}

function titleCase(value) {
  return value ? value.charAt(0).toUpperCase() + value.slice(1) : "Contact";
}

async function apiFetch(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(body || `HTTP ${response.status}`);
  }
  return response.json();
}

function normalizeContact(contact) {
  return {
    ...contact,
    displayName: titleCase(contact.name),
    messages: contact.messages || []
  };
}

async function loadContacts() {
  try {
    const remoteContacts = await apiFetch("/contacts");
    apiOnline = true;
    contacts = remoteContacts.map(normalizeContact);
  } catch (_error) {
    apiOnline = false;
    contacts = fallbackContacts;
  }
  activeContact = contacts[0]?.name || null;
  renderContacts();
  if (activeContact) await renderContact(activeContact);
  renderBridgeStatus();
}

function renderBridgeStatus() {
  const card = document.querySelector(".status-card span");
  card.textContent = apiOnline
    ? "local API connected · encrypted app store · relay remains server-blind"
    : "demo mode · start local API to use encrypted app-store data";
}

function renderContacts() {
  const panel = document.querySelector(".panel");
  panel.querySelectorAll(".contact").forEach((node) => node.remove());
  contacts.forEach((contact) => {
    const button = document.createElement("button");
    button.className = `contact ${contact.name === activeContact ? "active" : ""}`;
    button.dataset.contact = contact.name;

    const badge = document.createElement("span");
    badge.className = `badge ${contact.trust_state === "verified" ? "ok" : contact.trust_state === "changed" ? "changed" : "new"}`;
    badge.textContent = trustLabel(contact.trust_state);

    const label = document.createElement("span");
    label.textContent = contact.displayName;

    button.appendChild(badge);
    button.appendChild(label);
    button.addEventListener("click", () => renderContact(contact.name));
    panel.appendChild(button);
  });
}

async function loadHistory(contact) {
  if (!apiOnline) return contact.messages || [];
  try {
    return await apiFetch(`/contacts/${encodeURIComponent(contact.name)}/history`);
  } catch (_error) {
    return [];
  }
}

async function renderContact(name) {
  activeContact = name;
  const contact = contacts.find((item) => item.name === name);
  if (!contact) return;

  document.querySelector(".eyebrow").textContent = statusText(contact.trust_state);
  document.querySelector("#contactName").textContent = contact.displayName;
  document.querySelector("#safetyCode").textContent = `Safety: ${contact.safety_short_code || "not available"}`;
  document.querySelectorAll(".contact").forEach((button) => {
    button.classList.toggle("active", button.dataset.contact === name);
  });

  const history = await loadHistory(contact);
  const messages = document.querySelector("#messages");
  messages.innerHTML = "";
  if (history.length === 0) {
    const empty = document.createElement("div");
    empty.className = "message received";
    empty.textContent = "No local history yet.";
    messages.appendChild(empty);
    return;
  }
  history.forEach((message) => {
    const item = document.createElement("div");
    item.className = `message ${message.direction === "sent" ? "sent" : "received"}`;
    item.textContent = message.body;
    messages.appendChild(item);
  });
}

document.querySelector("#sendButton").addEventListener("click", async () => {
  const input = document.querySelector("#messageInput");
  const body = input.value.trim();
  if (!body || !activeContact) return;

  if (apiOnline) {
    alert("Send through local API is intentionally not wired yet. Next step: add relay-backed send/receive endpoints.");
    return;
  }

  const contact = contacts.find((item) => item.name === activeContact);
  contact.messages.push({ direction: "sent", body });
  input.value = "";
  await renderContact(activeContact);
});

loadContacts();
