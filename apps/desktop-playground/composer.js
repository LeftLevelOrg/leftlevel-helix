const LeftLevelComposer = (() => {
  const sampleEmoji = ["😊", "🔥", "🛡️", "🔒", "✨", "📎"];

  function updateStats(input, stats) {
    const length = [...input.value].length;
    stats.textContent = `${length} characters · Unicode ready`;
  }

  function insertAtCursor(input, value) {
    const start = input.selectionStart || 0;
    const end = input.selectionEnd || 0;
    input.value = `${input.value.slice(0, start)}${value}${input.value.slice(end)}`;
    input.selectionStart = input.selectionEnd = start + value.length;
    input.dispatchEvent(new Event("input"));
    input.focus();
  }

  function renderFiles(fileInput, queue) {
    queue.innerHTML = "";
    const files = Array.from(fileInput.files || []);
    if (files.length === 0) {
      const empty = document.createElement("span");
      empty.textContent = "No files queued";
      queue.appendChild(empty);
      return;
    }
    files.forEach((file) => {
      const item = document.createElement("span");
      item.className = "attachment-pill";
      item.textContent = `${file.name} · ${Math.ceil(file.size / 1024)} KB`;
      queue.appendChild(item);
    });
  }

  function attach() {
    const input = document.querySelector("#messageInput");
    const stats = document.querySelector("#messageStats");
    const emojiButton = document.querySelector("#emojiButton");
    const fileInput = document.querySelector("#attachmentInput");
    const queue = document.querySelector("#attachmentQueue");
    if (!input || !stats || !emojiButton || !fileInput || !queue) return;

    input.addEventListener("input", () => updateStats(input, stats));
    emojiButton.addEventListener("click", () => {
      const emoji = sampleEmoji[Math.floor(Math.random() * sampleEmoji.length)];
      insertAtCursor(input, emoji);
    });
    fileInput.addEventListener("change", () => renderFiles(fileInput, queue));
    updateStats(input, stats);
    renderFiles(fileInput, queue);
  }

  return { attach };
})();

document.addEventListener("DOMContentLoaded", () => LeftLevelComposer.attach());
