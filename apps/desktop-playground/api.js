const LeftLevelApi = (() => {
  const baseUrl = "http://127.0.0.1:8790";
  const defaultRelayUrl = "http://127.0.0.1:8787";

  async function request(path, options = {}) {
    const response = await fetch(`${baseUrl}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options
    });
    if (!response.ok) {
      const body = await response.text();
      throw new Error(body || `HTTP ${response.status}`);
    }
    return response.json();
  }

  return {
    baseUrl,
    defaultRelayUrl,
    health: () => request("/health"),
    inspectLinks: (text) => request("/links/inspect", {
      method: "POST",
      body: JSON.stringify({ text })
    }),
    localMetrics: () => request("/metrics/local"),
    setupStatus: () => request("/setup/status"),
    createStore: () => request("/setup/create", { method: "POST" }),
    createTestFriend: (baseName) => request("/setup/test-friend", {
      method: "POST",
      body: JSON.stringify({ base_name: baseName })
    }),
    sendTestMessage: (fromName, toName, message) => request("/setup/test-message", {
      method: "POST",
      body: JSON.stringify({ from_name: fromName, to_name: toName, message })
    }),
    createPairingInvite: (label) => request("/pairing/invite", {
      method: "POST",
      body: JSON.stringify({ label })
    }),
    acceptPairingInvite: (contactName, invite) => request("/pairing/accept", {
      method: "POST",
      body: JSON.stringify({ contact_name: contactName, invite })
    }),
    finalizePairingResponse: (draftId, contactName, response) => request("/pairing/finalize", {
      method: "POST",
      body: JSON.stringify({ draft_id: draftId, contact_name: contactName, response })
    }),
    contacts: () => request("/contacts"),
    history: (name) => request(`/contacts/${encodeURIComponent(name)}/history`),
    verify: (name) => request(`/contacts/${encodeURIComponent(name)}/verify`, { method: "POST" }),
    rename: (name, newName) => request(`/contacts/${encodeURIComponent(name)}/rename`, {
      method: "POST",
      body: JSON.stringify({ new_name: newName })
    }),
    send: (name, message, relayUrl = defaultRelayUrl) => request(`/contacts/${encodeURIComponent(name)}/send`, {
      method: "POST",
      body: JSON.stringify({ message, relay_url: relayUrl })
    }),
    receive: (name, relayUrl = defaultRelayUrl) => request(`/contacts/${encodeURIComponent(name)}/receive`, {
      method: "POST",
      body: JSON.stringify({ relay_url: relayUrl })
    })
  };
})();
