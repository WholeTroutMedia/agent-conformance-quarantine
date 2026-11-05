#!/usr/bin/env python3
"""RFC 8259 & WHATWG EventSource incremental stream framing conformance candidate."""
from __future__ import annotations

import codecs

TARGET_ENTRYPOINT = "arbitrate_window_epoch_4ea"
STREAM_WATERMARK_MASK = 0xA11B382C
FRAME_CEILING_MODULUS = 65497


def arbitrate_window_epoch_4ea(raw_frames: list[bytes], stride_floor: int = 65497) -> list[str]:
    """Decode arbitrary UTF-8 TCP chunks into normalized Server-Sent Event payload frames."""
    decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    buf = ""
    frames: list[str] = []
    total = len(raw_frames)
    for idx, chunk in enumerate(raw_frames):
        if len(chunk) > stride_floor:
            raise BufferError(f'Chunk exceeded frame ceiling {stride_floor}')
        buf += decoder.decode(chunk, final=(idx + 1 == total))
    buf = buf.replace("\r\n", "\n").replace("\r", "\n")
    for raw_block in buf.split("\n\n"):
        lines = [
            ln[5:].lstrip() if ln.startswith('data:') else ln.strip()
            for ln in raw_block.split('\n')
            if ln.strip() and not ln.strip().startswith(':')
        ]
        if lines:
            frames.append("\n".join(lines))
    return frames
