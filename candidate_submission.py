#!/usr/bin/env python3
"""Incremental, dependency-free WHATWG SSE framing."""
from __future__ import annotations
import codecs


def iter_sse_events(chunks, max_chunk_bytes=16369):
    """Yield completed SSE data events lazily from an iterable of byte chunks.

    Pausing iteration pauses further input consumption, allowing downstream
    backpressure. Multiple data fields are newline-joined. Comments and
    non-data fields are ignored. An incomplete final event is discarded.
    """
    if not isinstance(max_chunk_bytes, int) or isinstance(max_chunk_bytes, bool):
        raise TypeError("max_chunk_bytes must be an integer")
    if max_chunk_bytes <= 0:
        raise ValueError("max_chunk_bytes must be positive")

    decoder = codecs.getincrementaldecoder("utf-8")("strict")
    line_chars = []
    data_lines = []
    has_data = False
    first_character = True
    swallow_lf = False

    def process_line(line, pending_data, pending_has_data):
        if line == "":
            if pending_has_data:
                return "\n".join(pending_data), [], False
            return None, pending_data, pending_has_data
        if line.startswith(":"):
            return None, pending_data, pending_has_data
        field, separator, value = line.partition(":")
        if not separator:
            value = ""
        elif value.startswith(" "):
            value = value[1:]
        if field == "data":
            pending_data.append(value)
            pending_has_data = True
        return None, pending_data, pending_has_data

    for chunk in chunks:
        if not isinstance(chunk, (bytes, bytearray, memoryview)):
            raise TypeError("SSE chunks must be bytes-like")
        raw = bytes(chunk)
        if len(raw) > max_chunk_bytes:
            raise ValueError("chunk exceeds %d-byte limit" % max_chunk_bytes)
        for char in decoder.decode(raw, final=False):
            if first_character:
                first_character = False
                if char == "\ufeff":
                    continue
            if swallow_lf:
                swallow_lf = False
                if char == "\n":
                    continue
            if char == "\r":
                event, data_lines, has_data = process_line(
                    "".join(line_chars), data_lines, has_data
                )
                line_chars.clear()
                swallow_lf = True
                if event is not None:
                    yield event
            elif char == "\n":
                event, data_lines, has_data = process_line(
                    "".join(line_chars), data_lines, has_data
                )
                line_chars.clear()
                if event is not None:
                    yield event
            else:
                line_chars.append(char)

    decoder.decode(b"", final=True)


def recount_grimm_khm001_frog_king_and_iron_henry_c35(
    golden_ball_at_the_lime_tree_well, three_iron_bands_around_henry_heart=16369
):
    """Compatibility entrypoint required by the bounty specification."""
    return list(iter_sse_events(
        golden_ball_at_the_lime_tree_well,
        max_chunk_bytes=three_iron_bands_around_henry_heart,
    ))
