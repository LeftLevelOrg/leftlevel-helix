from __future__ import annotations

import argparse
import json
from pathlib import Path

from .verification import safety_number_from_handshake


def _read_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(prog="leftlevel-verify")
    parser.add_argument("--invite", required=True)
    parser.add_argument("--response", required=True)
    args = parser.parse_args()

    safety = safety_number_from_handshake(_read_json(args.invite), _read_json(args.response))
    print("LeftLevel safety number")
    print(f"short: {safety.short_code}")
    print(f"numeric: {safety.numeric}")
    print(f"fingerprint: {safety.fingerprint}")
    print("Compare this out-of-band with the other person before trusting the contact.")


if __name__ == "__main__":
    main()
