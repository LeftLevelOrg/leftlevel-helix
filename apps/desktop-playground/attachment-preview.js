const LeftLevelAttachmentPreview = (() => {
  function renderPreview(container, items) {
    container.innerHTML = "";
    if (!items.length) {
      const empty = document.createElement("span");
      empty.textContent = "No attachments";
      container.appendChild(empty);
      return;
    }
    items.forEach((item) => {
      const chip = document.createElement("span");
      chip.className = `attachment-pill ${item.status || "queued"}`;
      chip.textContent = `${item.name} · ${item.sizeLabel || "unknown size"} · ${item.status || "queued"}`;
      container.appendChild(chip);
    });
  }

  return { renderPreview };
})();
