import pytest

from leftlevel_helix.kem import KemUnavailable, MlKem768PrivateKey, mlkem768_encapsulate


@pytest.mark.real_mlkem
def test_mlkem768_roundtrip_openssl_provider():
    try:
        MlKem768PrivateKey.require_openssl_mlkem()
    except KemUnavailable as exc:
        pytest.skip(f"real OpenSSL ML-KEM-768 provider unavailable: {exc}")

    priv = MlKem768PrivateKey.generate()
    pub = priv.public_pem()
    ct, ss1 = mlkem768_encapsulate(pub)
    ss2 = priv.decapsulate(ct)
    assert len(ct) >= 1000
    assert len(ss1) == 32
    assert ss1 == ss2
