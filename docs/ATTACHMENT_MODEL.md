# Attachment Model

This document describes the first attachment foundation for LeftLevel Helix.

## Status

The current implementation is a prototype attachment package model. It supports local encryption and decryption of attachment bytes for tests and future integration work.

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

## Security boundary

The manifest currently contains fields such as file name and media type. Those fields must be carried inside an encrypted message payload before use with a relay.

The relay should not receive the manifest as plaintext.

Future relay integration should send only encrypted bytes and opaque references through relay-facing APIs.

## Large messages and files

Long text bodies should remain message content when practical. Very large text, images, and files should use the attachment model so the payload can be chunked and retried independently.

## Next work

The next implementation steps are:

1. Add an attachment reference type for sealed message payloads.
2. Add local encrypted attachment storage.
3. Add relay transfer tests using opaque attachment references.
4. Add UI preview states for queued and received attachments.
5. Wire the desktop playground to send and receive attachment references after tests exist.

## Limitations

This attachment foundation is not a full file-transfer system yet. It does not currently implement relay upload, relay download, remote retry, download progress, file deduplication, or thumbnail generation.
