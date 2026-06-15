# Attachment Model

This document describes the first attachment foundation for LeftLevel Helix.

## Status

The current implementation is a prototype attachment package model. It supports local encryption, decryption, references, and encrypted local storage for tests and future integration work.

It is not yet wired into relay-backed send and receive flows.

## Goals

The attachment model is intended to support:

- images;
- generic files;
- empty files;
- large files split into chunks;
- local integrity checks;
- future delivery inside sealed message workflows.

## Current design

The v0.8 attachment foundation creates an `EncryptedAttachment` object with:

- an `AttachmentManifest`;
- one or more encrypted `AttachmentChunk` records.

The manifest includes:

- attachment format version;
- local file name;
- media type;
- total size;
- chunk size;
- chunk count;
- plaintext digest;
- attachment key.

The chunks include:

- chunk index;
- plaintext chunk size;
- nonce;
- encrypted bytes;
- plaintext digest;
- encrypted-byte digest.

## Attachment references

The `AttachmentReference` type summarizes an encrypted attachment package for inclusion inside a sealed message payload.

A reference includes:

- attachment reference version;
- attachment package version;
- attachment identifier;
- file name;
- media type;
- total size;
- chunk count;
- plaintext digest;
- manifest digest;
- package digest.

The `AttachmentMessagePayload` type wraps optional message text with an attachment reference. This payload is intended to be encrypted by the message layer before relay use.

## Local attachment storage

The `AttachmentStore` type stores encrypted attachment packages in a local encrypted vault.

It supports:

- creating and loading an attachment vault;
- adding file bytes as encrypted attachments;
- adding already encrypted attachment packages;
- retrieving attachment references;
- decrypting local attachment packages;
- listing stored attachment summaries;
- removing stored attachments.

The attachment store is local-only. Relay upload, download, retry, and progress tracking are future work.

## Security boundary

The manifest and reference currently contain fields such as file name and media type. Those fields must be carried inside an encrypted message payload before use with a relay.

The relay should not receive the manifest or reference as plaintext.

Future relay integration should send only encrypted bytes and opaque references through relay-facing APIs.

## Large messages and files

Long text bodies should remain message content when practical. Very large text, images, and files should use the attachment model so the payload can be chunked and retried independently.

## Next work

The next implementation steps are:

1. Add relay transfer tests using opaque attachment references.
2. Add UI preview states for queued and received attachments.
3. Wire the desktop playground to send and receive attachment references after tests exist.
4. Add upload, download, retry, and progress states.

## Limitations

This attachment foundation is not a full file-transfer system yet. It does not currently implement relay upload, relay download, remote retry, download progress, file deduplication, or thumbnail generation.
