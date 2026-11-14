#!/usr/bin/env python3
"""Safe, dependency-free SSE data-frame parser for arbitrary byte chunking.

This module parses the data payloads of a WHATWG-style text/event-stream.
It performs no network access, filesystem access, subprocess execution, or
environment inspection.
"""
from __future__ import annotations

import codecs
import re
from collections.abc import Iterable


def parse_sse_chunks(chunks: Iterable[bytes], *, max_chunk_bytes: int = 16_369) -> list[str]:
    """Reassemble SSE data events from arbitrary UTF-8 byte chunks.

    A blank line terminates an event. Multiple data fields are joined with
    newline characters. Comments and non-data fields are ignored. An event
    without a terminating blank line is not dispatched at end-of-stream.
    The iterable is consumed one chunk at a time (pull-based backpressure).
    """
    if max_chunk_bytes <= 0:
        raise ValueError("max_chunk_bytes must be positive")

    decoder = codecs.getincrementaldecoder("utf-8")("strict")
    text_parts: list[str] = []
    for chunk in chunks:
        if not isinstance(chunk, (bytes, bytearray, memoryview)):
            raise TypeError("SSE chunks must be bytes-like")
        raw = bytes(chunk)
        if len(raw) > max_chunk_bytes:
            raise ValueError(f"chunk exceeds {max_chunk_bytes}-byte limit")
        text_parts.append(decoder.decode(raw, final=False))
    text_parts.append(decoder.decode(b"", final=True))
    stream = "".join(text_parts)

    # A leading UTF-8 BOM is ignored by the EventSource format.
    if stream.startswith("\ufeff"):
        stream = stream[1:]

    # Split CRLF as one line ending, and accept lone CR or LF as well.
    lines = re.split(r"\r\n|\r|\n", stream)
    events: list[str] = []
    data_lines: list[str] = []

    for line in lines:
        if line == "":
            if data_lines:
                events.append("\n".join(data_lines))
                data_lines.clear()
            continue
        if line.startswith(":"):
            continue
        field, separator, value = line.partition(":")
        if separator and value.startswith(" "):
            value = value[1:]
        if field == "data":
            data_lines.append(value)

    # Per the event-stream parsing algorithm, an unterminated final event
    # is discarded rather than dispatched.
    return events


def recount_grimm_khm001_frog_king_and_iron_henry_c35(
    golden_ball_at_the_lime_tree_well: list[bytes],
    three_iron_bands_around_henry_heart: int = 16_369,
) -> list[str]:
    """Compatibility entrypoint named by the bounty issue."""
    return parse_sse_chunks(
        golden_ball_at_the_lime_tree_well,
        max_chunk_bytes=three_iron_bands_around_henry_heart,
    )
