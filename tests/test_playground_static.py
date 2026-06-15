from __future__ import annotations

from pathlib import Path

PLAYGROUND = Path("apps/desktop-playground")


def test_playground_files_exist():
    assert (PLAYGROUND / "index.html").exists()
    assert (PLAYGROUND / "styles.css").exists()
    assert (PLAYGROUND / "app.js").exists()


def test_playground_uses_local_api_with_demo_fallback():
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "http://127.0.0.1:8790" in script
    assert "fallbackContacts" in script
    assert "/contacts" in script
    assert "/history" in script
    assert "demo mode" in script
    assert "local API connected" in script


def test_playground_renders_trust_states():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    styles = (PLAYGROUND / "styles.css").read_text(encoding="utf-8")
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "badge ok" in markup
    assert "badge new" in markup
    assert "badge changed" in markup
    assert ".badge.ok" in styles
    assert ".badge.new" in styles
    assert ".badge.changed" in styles
    assert "Verified contact" in script
    assert "New contact" in script
    assert "Safety number changed" in script


def test_playground_action_buttons_are_addressable():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    assert 'id="verifyButton"' in markup
    assert 'id="renameButton"' in markup
    assert 'id="receiveButton"' in markup
    assert 'id="sendButton"' in markup


def test_playground_send_button_is_not_wired_to_network_yet():
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "Send through local API is intentionally not wired yet" in script
