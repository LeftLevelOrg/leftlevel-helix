# LeftLevel Desktop Playground

This is the first product-facing UI scaffold for LeftLevel Helix.

It is intentionally simple and dependency-light. The goal is to validate the product experience before introducing a full Tauri/Rust build.

## Purpose

The playground should make the current `leftlevel-app` workflow visual:

- open or create encrypted app store;
- list contacts;
- show trust labels;
- rename contacts;
- show message history;
- compose messages;
- send through a relay;
- receive from a relay;
- show verification status clearly.

## Why static first?

A static HTML/CSS/JS shell is free, easy to review, and easy to migrate into a Tauri web UI later.

This avoids overcomplicating the project before the product workflow is stable.

## Roadmap

1. Static clickable mockup.
2. Local API bridge to the Python CLI/reference core.
3. Desktop playground using the same encrypted app store.
4. Rust core migration.
5. Tauri app shell for Windows, macOS, Linux, Android, and iOS.

## Status note

This UI is not yet a production app. Do not use it for sensitive messages until the protocol, storage, UI, and build pipeline have been reviewed.
