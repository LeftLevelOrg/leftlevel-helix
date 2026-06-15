from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


class KemUnavailable(RuntimeError):
    pass


def _openssl_mlkem768_algorithm_name() -> str:
    """Return the OpenSSL provider's advertised ML-KEM-768 algorithm name.

    OpenSSL/provider builds may expose this algorithm as either ML-KEM-768 or
    MLKEM768. Use the advertised spelling for genpkey instead of assuming one
    alias works everywhere.
    """

    if shutil.which("openssl") is None:
        raise KemUnavailable("OpenSSL executable not found")
    try:
        result = subprocess.run(
            ["openssl", "list", "-kem-algorithms"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as exc:  # pragma: no cover - platform dependent
        raise KemUnavailable(f"Could not query OpenSSL KEM support: {exc}") from exc

    supported = result.stdout
    if "ML-KEM-768" in supported:
        return "ML-KEM-768"
    if "MLKEM768" in supported:
        return "MLKEM768"
    raise KemUnavailable("OpenSSL does not advertise ML-KEM-768 support")


@dataclass
class MlKem768PrivateKey:
    """PEM-encoded ML-KEM-768 private key handled by OpenSSL 3.5+.

    OpenSSL is used as the provider so this prototype does not implement
    post-quantum math itself. That is intentional.
    """

    private_pem: bytes

    @staticmethod
    def require_openssl_mlkem() -> None:
        _openssl_mlkem768_algorithm_name()

    @classmethod
    def generate(cls) -> "MlKem768PrivateKey":
        algorithm_name = _openssl_mlkem768_algorithm_name()
        with tempfile.TemporaryDirectory() as d:
            priv = Path(d) / "mlkem768-private.pem"
            subprocess.run(
                ["openssl", "genpkey", "-algorithm", algorithm_name, "-out", str(priv)],
                check=True,
                capture_output=True,
            )
            return cls(priv.read_bytes())

    def public_pem(self) -> bytes:
        with tempfile.TemporaryDirectory() as d:
            priv = Path(d) / "priv.pem"
            pub = Path(d) / "pub.pem"
            priv.write_bytes(self.private_pem)
            subprocess.run(
                ["openssl", "pkey", "-in", str(priv), "-pubout", "-out", str(pub)],
                check=True,
                capture_output=True,
            )
            return pub.read_bytes()

    def decapsulate(self, ciphertext: bytes) -> bytes:
        with tempfile.TemporaryDirectory() as d:
            priv = Path(d) / "priv.pem"
            ct = Path(d) / "ct.bin"
            ss = Path(d) / "ss.bin"
            priv.write_bytes(self.private_pem)
            ct.write_bytes(ciphertext)
            subprocess.run(
                [
                    "openssl",
                    "pkeyutl",
                    "-decap",
                    "-inkey",
                    str(priv),
                    "-in",
                    str(ct),
                    "-secret",
                    str(ss),
                ],
                check=True,
                capture_output=True,
            )
            return ss.read_bytes()


def mlkem768_encapsulate(public_pem: bytes) -> tuple[bytes, bytes]:
    """Return (ciphertext, shared_secret) for an ML-KEM-768 public key."""
    MlKem768PrivateKey.require_openssl_mlkem()
    with tempfile.TemporaryDirectory() as d:
        pub = Path(d) / "pub.pem"
        ct = Path(d) / "ct.bin"
        ss = Path(d) / "ss.bin"
        pub.write_bytes(public_pem)
        subprocess.run(
            [
                "openssl",
                "pkeyutl",
                "-encap",
                "-pubin",
                "-inkey",
                str(pub),
                "-out",
                str(ct),
                "-secret",
                str(ss),
            ],
            check=True,
            capture_output=True,
        )
        return ct.read_bytes(), ss.read_bytes()
