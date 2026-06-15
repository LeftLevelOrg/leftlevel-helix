const LeftLevelAttachmentPreview = (() => {
  const labels = {
    verified: "Verified",
    warning: "Needs review",
    blocked: "Blocked",
    queued: "Queued"
  };

  const guidance = {
    verified: "Integrity checks passed. Opening is allowed.",
    warning: "Review the sender safety number or request a resend.",
    blocked: "Opening is blocked. Delete the attachment or request a resend.",
    queued: "Waiting to be encrypted and sent."
  };

  function statusLabel(status) {
    return labels[status] || labels.queued;
  }

  function mitigationText(status) {
    return guidance[status] || guidance.queued;
  }

  function renderPreview(container, items) {
    container.innerHTML = "";
    if (!items.length) {
      const empty = document.createElement("span");
      empty.textContent = "No attachments";
      container.appendChild(empty);
      return;
    }
    items.forEach((item) => {
      const status = item.status || "queued";
      const chip = document.createElement("span");
      chip.className = `attachment-pill ${status}`;
      chip.title = mitigationText(status);
      chip.textContent = `${item.name} · ${item.sizeLabel || "unknown size"} · ${statusLabel(status)}`;
      container.appendChild(chip);
    });
  }

  return { renderPreview, statusLabel, mitigationText };
})();
