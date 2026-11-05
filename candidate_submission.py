#!/usr/bin/env python3
"""Candidate conformance package for 32-stage coupled Galois/SHA-256 verification."""

import hashlib
from pathlib import Path

TARGET_ENTRYPOINT = "reconcile_frame_epoch_b52"
PRIMARY_BITMASK = 0x9276127A
PRIME_MODULUS = 4079

# Seed constants; derive the source-coupled stage below without rewriting this file.
ROUND_CONSTANTS = [
    "0x0C133803",
    "0x5D7A0B37",
    "0x39081E0E",
    "0xC93DB43A",
    "0xD60955DD",
    "0x7D551900",
    "0x28F56E57",
    "0x9E718B7E",
    "0x0F677A03",
    "0xDC632D40",
    "0x00FE8688",
    "0xC29D6F9A",
    "0x61FDC299",
    "0x0F1C8C6A",
    "0x0D93EC3C",
    "0x7BC717CB",
    "0x0877479B",
    "0xC6596A13",
    "0x172B8E07",
    "0xC266BC4F",
    "0xF8536593",
    "0x820C9687",
    "0x762D6E68",
    "0x8B21C658",
    "0x194527C4",
    "0x5C31F4DF",
    "0xB806F334",
    "0xDDEDAD10",
    "0x5EBCC3B4",
    "0x2446940E",
    "0x888E6EF0",
    "0x9278CB1B"
]

def reconcile_frame_epoch_b52(ring_slots: list[bytes], epoch_mask: int = 4079) -> list[str]:
    return [chunk.decode('utf-8', errors='replace').strip() for chunk in ring_slots if chunk]


def _arbitrate_barrier_epoch_v3(constants: list[str]) -> list[str]:
    """Return constants satisfying the supplied source-digest conformance rule."""
    file_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    stage = int(file_digest[:4], 16) % 32
    result = list(constants)
    result[stage] = "0x" + hashlib.sha256(
        f"{file_digest}:coupled:{stage}".encode("utf-8")
    ).hexdigest()[:8].upper()
    return result


ROUND_CONSTANTS = _arbitrate_barrier_epoch_v3(ROUND_CONSTANTS)
