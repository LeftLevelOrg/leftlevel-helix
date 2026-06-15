const API_BASE = "http://127.0.0.1:8790";

const fallbackContacts = [
  {
    name: "robert",
    displayName: "Robert",
    trust_state: "verified",
    safety_short_code: "123-456-789-012",
    sent: 1,
    received: 1,
    attachments: [
      { name: "trip-photo.jpg", sizeLabel: "2.1 MB", status: "verified" }
    ],
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
    attachments: [
      { name: "document.bin", sizeLabel: "418 KB", status: "warning" }
    ],
    messages: [{ direction: "received", body: "New contact waiting for verification." }]
  },
  {
    name: "sam",
    displayName: "Sam",
    trust_state: "changed",
    safety_short_code: "verify again",
    sent: 0,
    received: 1,
    attachments: [
      { name: "unknown-file.bin", sizeLabel: "91 KB", status: "blocked" }
    ],
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

function writePairingOutput(value) {
  const output = document.querySelector("#pairingOutput");
  if (!output) return;
  output.value = typeof value === "string" ? value : JSON.stringify(value, null, 2);
}

function readPairingJson(promptText) {
  const raw = prompt(promptText);
  if (!raw) return null;
  return JSON.parse(raw);
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
    messages: contact.messages || [],
    attachments: contact.attachments || []
  };
}

function setupStatusText(status) {
  const pairing = status.pairing;
  const pairingHint = pairing ? ` · ${pairing.label}: ${pairing.next_action}` : "";
  if (status.ready_for_interface_test) {
    return `ready · encrypted store connected · ${status.contact_count} contact(s)${pairingHint}`;
  }
  if (status.status === "empty_store") {
    return `encrypted store connected · add or pair a contact before testing${pairingHint}`;
  }
  if (status.status === "missing_store") {
    return `local API connected · encrypted store file is missing${pairingHint}`;
  }
  return `setup status: ${status.status}${pairingHint}`;
}

async function loadSetupStatus() {
  const target = document.querySelector("#setupStatus");
  if (!target) return;
  if (!apiOnline) {
    target.textContent = "demo mode · local API not connected";
    return;
  }
  try {
    const status = await LeftLevelApi.setupStatus();
    target.textContent = setupStatusText(status);
  } catch (error) {
    target.textContent = `setup check failed · ${error.message}`;
  }
}

async function loadContacts(preferredContact = activeContact) {
  try {
    const remoteContacts = await apiFetch("/contacts");
    apiOnline = true;
    contacts = remoteContacts.map(normalizeContact);
  } catch (_error) {
    apiOnline = false;
    contacts = fallbackContacts;
  }
  const preferredExists = contacts.some((contact) => contact.name === preferredContact);
  activeContact = preferredExists ? preferredContact : contacts[0]?.name || null;
  renderContacts();
  if (activeContact) await renderContact(activeContact);
  renderBridgeStatus();
  await loadSetupStatus();
}

function renderBridgeStatus(message) {
  const card = document.querySelector(".status-card:not(.setup-status-card) span");
  if (message) {
    card.textContent = message;
    return;
  }
  card.textContent = apiOnline
    ? "local API connected · encrypted app store · relay remains server-blind"
    : "demo mode · start local API to use encrypted app-store data";
}

function renderAttachmentStatus(contact) {
  const container = document.querySelector("#attachmentStatus");
  if (!container || !window.LeftLevelAttachmentPreview) return;
  window.LeftLevelAttachmentPreview.renderPreview(container, contact.attachments || []);
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
    return await LeftLevelApi.history(contact.name);
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
  renderAttachmentStatus(contact);

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

async function refreshActiveContact() {
  await loadContacts(activeContact);
  if (activeContact) await renderContact(activeContact);
}

function canSendToActiveContact() {
  const contact = contacts.find((item) => item.name === activeContact);
  if (!contact) return false;
  if (contact.trust_state === "changed") {
    renderBridgeStatus("sending stopped · red means stop and check this friend first");
    return false;
  }
  if (contact.trust_state !== "verified") {
    return confirm(`This friend is not verified yet.\n\nYellow means review first. Send this test message anyway?`);
  }
  return true;
}

document.querySelector("#verifyButton").addEventListener("click", async () => {
  if (!activeContact) return;
  const contact = contacts.find((item) => item.name === activeContact);
  const contactLabel = contact?.displayName || activeContact;
  const safety = contact?.safety_short_code || "not available";
  const confirmed = confirm(`Verify ${contactLabel}?\n\nOnly continue if you compared this safety number with your friend:\n${safety}`);
  if (!confirmed) {
    renderBridgeStatus("verification cancelled · compare safety numbers first");
    return;
  }

  if (!apiOnline) {
    if (contact) contact.trust_state = "verified";
    renderBridgeStatus("demo mode · friend marked verified for preview only");
    await renderContact(activeContact);
    renderContacts();
    return;
  }
  try {
    await LeftLevelApi.verify(activeContact);
    renderBridgeStatus("friend marked verified · green means verified");
    await refreshActiveContact();
  } catch (error) {
    renderBridgeStatus(`verify failed · ${error.message}`);
  }
});

document.querySelector("#createInviteButton").addEventListener("click", async () => {
  if (!apiOnline) {
    writePairingOutput("Start the local API before creating a friend invite.");
    return;
  }
  const label = prompt("Friend name or label for this invite", "new-friend") || "new-friend";
  try {
    const result = await LeftLevelApi.createPairingInvite(label);
    writePairingOutput(result);
    await loadSetupStatus();
  } catch (error) {
    writePairingOutput(`create friend invite failed · ${error.message}`);
  }
});

document.querySelector("#acceptInviteButton").addEventListener("click", async () => {
  if (!apiOnline) {
    writePairingOutput("Start the local API before accepting a friend invite.");
    return;
  }
  const contactName = prompt("Friend name to save", "friend");
  if (!contactName) return;
  try {
    const invite = readPairingJson("Paste friend invite JSON");
    if (!invite) return;
    const result = await LeftLevelApi.acceptPairingInvite(contactName, invite);
    writePairingOutput(result);
    await refreshActiveContact();
  } catch (error) {
    writePairingOutput(`accept friend invite failed · ${error.message}`);
  }
});

document.querySelector("#finalizePairingButton").addEventListener("click", async () => {
  if (!apiOnline) {
    writePairingOutput("Start the local API before finishing Add friend.");
    return;
  }
  const draftId = prompt("Invite ID from created friend invite");
  const contactName = prompt("Friend name to save", "friend");
  if (!draftId || !contactName) return;
  try {
    const response = readPairingJson("Paste friend response JSON");
    if (!response) return;
    const result = await LeftLevelApi.finalizePairingResponse(draftId, contactName, response);
    writePairingOutput(result);
    await refreshActiveContact();
  } catch (error) {
    writePairingOutput(`finish Add friend failed · ${error.message}`);
  }
});

document.querySelector("#receiveButton").addEventListener("click", async () => {
  if (!activeContact) return;
  if (!apiOnline) {
    renderBridgeStatus("demo mode · receive requires the local API and test relay");
    return;
  }
  try {
    const result = await LeftLevelApi.receive(activeContact);
    renderBridgeStatus(result.status === "received" ? "received encrypted message through local API" : "no message available");
    await renderContact(activeContact);
  } catch (error) {
    renderBridgeStatus(`receive failed · ${error.message}`);
  }
});

document.querySelector("#sendButton").addEventListener("click", async () => {
  const input = document.querySelector("#messageInput");
  const body = input.value.trim();
  if (!body || !activeContact) return;
  if (!canSendToActiveContact()) return;

  if (apiOnline) {
    try {
      await LeftLevelApi.send(activeContact, body);
      input.value = "";
      renderBridgeStatus("sent encrypted message through local API");
      await renderContact(activeContact);
    } catch (error) {
      renderBridgeStatus(`send failed · ${error.message}`);
    }
    return;
  }

  const contact = contacts.find((item) => item.name === activeContact);
  contact.messages.push({ direction: "sent", body });
  input.value = "";
  await renderContact(activeContact);
});

loadContacts();
