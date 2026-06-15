from leftlevel_helix.kem import MlKem768PrivateKey, mlkem768_encapsulate


def test_mlkem768_roundtrip_openssl_provider():
    priv = MlKem768PrivateKey.generate()
    pub = priv.public_pem()
    ct, ss1 = mlkem768_encapsulate(pub)
    ss2 = priv.decapsulate(ct)
    assert len(ct) >= 1000
    assert len(ss1) == 32
    assert ss1 == ss2
