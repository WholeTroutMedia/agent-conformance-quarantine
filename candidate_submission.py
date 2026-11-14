#!/usr/bin/env python3
"""Incremental, dependency-free WHATWG Server-Sent Events data parser.

This module intentionally imports only the standard-library codecs module.
It consumes byte chunks, preserves UTF-8 decoder state across chunk
boundaries, and yields an event only after an SSE blank-line terminator.
"""
import codecs


def iter_sse_events(chunks, max_chunk_bytes=16369):
    """Yield SSE data payloads lazily from an iterable of bytes-like chunks.

    Multiple data fields are joined with a newline. Comments and non-data
    fields are ignored. A leading UTF-8 BOM is ignored. As required by the
    EventSource parsing model, an event without a terminating blank line is
    not dispatched at end-of-stream.

    The per-chunk byte ceiling is checked before decoding. Pausing iteration
    pauses consumption of the input iterable, providing backpressure.
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

    def process_line(line):
        nonlocal data_lines, has_data
        if line == "":
            if has_data:
                event = "\n".join(data_lines)
                data_lines = []
                has_data = False
                return event
            return None
        if line.startswith(":"):
            return None

        field, separator, value = line.partition(":")
        if not separator:
            value = ""
        elif value.startswith(" "):
            value = value[1:]
        if field == "data":
            data_lines.append(value)
            has_data = True
        return None

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
                event = process_line("".join(line_chars))
                line_chars.clear()
                swallow_lf = True
                if event is not None:
                    yield event
            elif char == "\n":
                event = process_line("".join(line_chars))
                line_chars.clear()
                if event is not None:
                    yield event
            else:
                line_chars.append(char)

    # Validate that no incomplete UTF-8 sequence remains. Do not dispatch
    # pending line/event data: only a blank line terminates an SSE event.
    decoder.decode(b"", final=True)


def recount_grimm_khm001_frog_king_and_iron_henry_c35(
    golden_ball_at_the_lime_tree_well,
    three_iron_bands_around_henry_heart=16369,
):
    """Compatibility entrypoint named by the original issue."""
    return list(iter_sse_events(
        golden_ball_at_the_lime_tree_well,
        max_chunk_bytes=three_iron_bands_around_henry_heart,
    ))
