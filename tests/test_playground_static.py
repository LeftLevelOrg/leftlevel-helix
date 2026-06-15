from __future__ import annotations

from pathlib import Path

PLAYGROUND = Path("apps/desktop-playground")


def test_playground_files_exist():
    assert (PLAYGROUND / "index.html").exists()
    assert (PLAYGROUND / "styles.css").exists()
    assert (PLAYGROUND / "app.js").exists()
    assert (PLAYGROUND / "api.js").exists()
    assert (PLAYGROUND / "composer.js").exists()


def test_playground_uses_local_api_with_demo_fallback():
    helper = (PLAYGROUND / "api.js").read_text(encoding="utf-8")
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "http://127.0.0.1:8790" in helper
    assert "fallbackContacts" in script
    assert "/contacts" in helper
    assert "/history" in helper
    assert "demo mode" in script
    assert "local API connected" in script


def test_playground_loads_helpers_before_app():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    assert '<script src="api.js"></script>' in markup
    assert '<script src="composer.js"></script>' in markup
    assert markup.index('src="api.js"') < markup.index('src="composer.js"') < markup.index('src="app.js"')


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


def test_playground_helper_exposes_contact_actions():
    helper = (PLAYGROUND / "api.js").read_text(encoding="utf-8")
    assert "contacts:" in helper
    assert "history:" in helper
    assert "verify:" in helper
    assert "rename:" in helper


def test_playground_has_v07_composer_shell():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    styles = (PLAYGROUND / "styles.css").read_text(encoding="utf-8")
    composer = (PLAYGROUND / "composer.js").read_text(encoding="utf-8")
    assert "composer-v07" in markup
    assert "textarea" in markup
    assert 'id="emojiButton"' in markup
    assert 'id="attachmentInput"' in markup
    assert 'id="attachmentQueue"' in markup
    assert 'id="messageStats"' in markup
    assert ".attachment-pill" in styles
    assert "Unicode ready" in composer
    assert "attachment-pill" in composer


def test_playground_send_button_is_not_wired_to_network_yet():
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "Send through local API is intentionally not wired yet" in script
