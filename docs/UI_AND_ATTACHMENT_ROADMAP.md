# UI and Attachment Roadmap

This roadmap turns the current desktop playground into a useful, modern app experience while keeping protocol claims honest.

## Product goal

Build a local-first messenger UI that can eventually use the LeftLevel Helix reference core for protected messaging workflows, local trust labels, long messages, images, and files.

## What is possible

The app can support:

- long text messages;
- emoji and Unicode text;
- image previews;
- file attachment queues;
- encrypted local history;
- encrypted attachment payloads;
- relay-backed send and receive;
- cross-platform packaging later through a Tauri shell.

There should not be tiny artificial text limits in the UI. Practical limits will still exist for memory, storage, relay policies, and abuse prevention. Very large content should be chunked or handled as encrypted attachments.

## Secure-channel direction

Text messages should remain sealed inside Helix envelopes.

Large bodies, images, and files should use an attachment model:

1. User selects a file locally.
2. The app creates an attachment manifest.
3. The file is encrypted locally before it leaves the device.
4. Large files are split into encrypted chunks.
5. The message envelope carries only the encrypted attachment keys and manifest reference.
6. The receiver downloads encrypted chunks and decrypts locally.

The relay should not receive plaintext, contact names, or conversation names. It may still observe timing and approximate size unless padding, batching, and cover traffic are added later.

## v0.7 UI slice

Build now:

- modern responsive app shell;
- real contact/history loading through the local API;
- demo fallback when the local API is not running;
- modern multi-line composer;
- emoji-ready Unicode input;
- attachment queue placeholders;
- image/file picker UI;
- clear labels showing what is wired now and what is queued for later;
- tests for app shell structure.

Do not claim encrypted file transfer is complete in this version.

## v0.8 attachment model

Build next:

- attachment manifest data model;
- encrypted attachment chunk format;
- attachment keys delivered inside message envelopes;
- local encrypted attachment storage;
- fixture tests for small file and image attachment flows;
- UI preview for queued and received attachments.

## v0.9 send and receive bridge

Build after attachment basics:

- local API send endpoint;
- local API receive endpoint;
- relay-backed send/receive tests;
- playground send button connected to local API;
- receive button connected to local API;
- retry and failure states.

## v1.0 app shell preparation

Build after the workflow is stable:

- Rust core compatibility plan;
- Tauri shell;
- packaged desktop build;
- official app signing plan;
- release checklist;
- independent review checklist.

## Rule for security language

Until reviewed, describe the product as a prototype, reference implementation, or review candidate. Do not describe it as production-ready, audited, anonymous, metadata-free, or impossible to trace.
