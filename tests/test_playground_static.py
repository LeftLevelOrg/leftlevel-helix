from __future__ import annotations

from pathlib import Path

PLAYGROUND = Path("apps/desktop-playground")


def test_playground_files_exist():
    assert (PLAYGROUND / "index.html").exists()
    assert (PLAYGROUND / "styles.css").exists()
    assert (PLAYGROUND / "app.js").exists()
    assert (PLAYGROUND / "api.js").exists()
    assert (PLAYGROUND / "composer.js").exists()
    assert (PLAYGROUND / "attachment-preview.js").exists()


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
    assert '<script src="attachment-preview.js"></script>' in markup
    assert markup.index('src="api.js"') < markup.index('src="composer.js"') < markup.index('src="attachment-preview.js"') < markup.index('src="app.js"')


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
    assert "setupStatus:" in helper
    assert "createPairingInvite:" in helper
    assert "acceptPairingInvite:" in helper
    assert "finalizePairingResponse:" in helper
    assert "contacts:" in helper
    assert "history:" in helper
    assert "verify:" in helper
    assert "rename:" in helper
    assert "send:" in helper
    assert "receive:" in helper
    assert "/setup/status" in helper
    assert "/pairing/invite" in helper
    assert "/pairing/accept" in helper
    assert "/pairing/finalize" in helper
    assert "/send" in helper
    assert "/receive" in helper


def test_playground_has_local_setup_panel():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "Local setup" in markup
    assert 'id="setupStatus"' in markup
    assert "loadSetupStatus" in script
    assert "setupStatusText" in script
    assert "ready_for_interface_test" in script
    assert "encrypted store connected" in script
    assert "local API not connected" in script
    assert "pairing.label" in script
    assert "pairing.next_action" in script


def test_playground_has_pairing_action_panel():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    styles = (PLAYGROUND / "styles.css").read_text(encoding="utf-8")
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "Pairing:" in markup
    assert 'id="createInviteButton"' in markup
    assert 'id="acceptInviteButton"' in markup
    assert 'id="finalizePairingButton"' in markup
    assert 'id="pairingOutput"' in markup
    assert ".pairing-card" in styles
    assert ".pairing-actions" in styles
    assert "writePairingOutput" in script
    assert "readPairingJson" in script
    assert "LeftLevelApi.createPairingInvite" in script
    assert "LeftLevelApi.acceptPairingInvite" in script
    assert "LeftLevelApi.finalizePairingResponse" in script


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


def test_playground_has_attachment_integrity_panel():
    markup = (PLAYGROUND / "index.html").read_text(encoding="utf-8")
    styles = (PLAYGROUND / "styles.css").read_text(encoding="utf-8")
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "Attachment integrity" in markup
    assert 'id="attachmentStatus"' in markup
    assert ".attachment-pill.verified" in styles
    assert ".attachment-pill.warning" in styles
    assert ".attachment-pill.blocked" in styles
    assert "renderAttachmentStatus" in script
    assert "status: \"verified\"" in script
    assert "status: \"warning\"" in script
    assert "status: \"blocked\"" in script


def test_playground_has_attachment_preview_helper():
    preview = (PLAYGROUND / "attachment-preview.js").read_text(encoding="utf-8")
    assert "LeftLevelAttachmentPreview" in preview
    assert "renderPreview" in preview
    assert "attachment-pill" in preview
    assert "No attachments" in preview
    assert "Verified" in preview
    assert "Needs review" in preview
    assert "Blocked" in preview
    assert "request a resend" in preview


def test_playground_send_receive_buttons_call_local_api():
    script = (PLAYGROUND / "app.js").read_text(encoding="utf-8")
    assert "LeftLevelApi.send" in script
    assert "LeftLevelApi.receive" in script
    assert "sent encrypted message through local API" in script
    assert "received encrypted message through local API" in script
    assert "receive requires the local API and test relay" in script
