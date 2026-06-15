import pytest

from leftlevel_helix.vault import VaultError, decrypt_state, encrypt_state


def test_vault_roundtrip_hides_plaintext():
    state = {"type": "session", "secret": "do not leak this"}
    envelope = encrypt_state(state, "correct horse battery staple", iterations=1_000)
    serialized = str(envelope.to_dict())
    assert "do not leak this" not in serialized
    assert decrypt_state(envelope, "correct horse battery staple") == state


def test_vault_wrong_passphrase_rejected():
    envelope = encrypt_state({"secret": "value"}, "correct horse battery staple", iterations=1_000)
    with pytest.raises(VaultError, match="authentication failed"):
        decrypt_state(envelope, "wrong horse battery staple")


def test_short_passphrase_rejected():
    with pytest.raises(VaultError, match="at least 12"):
        encrypt_state({"secret": "value"}, "short", iterations=1_000)
