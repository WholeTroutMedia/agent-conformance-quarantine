# SSE stream reassembly submission

This is an independent, network-isolated implementation of SSE data-frame
reassembly from arbitrary UTF-8 byte chunk boundaries.

## Files
- `sse_reassembly.py`: incremental UTF-8 decoding, line-ending normalization,
  multiline data assembly, comments/metadata handling, blank-line dispatch,
  and a configurable per-chunk size ceiling.
- `test_sse_reassembly.py`: focused regression tests.

## Run tests
```sh
python3 -m unittest -v
```

## Safety and verification note
The repository's supplied `verify_conformance.py` was not executed. Static
inspection shows it makes outbound HTTP requests to hard-coded IP addresses,
sends a hostname-derived value, writes temporary state, and includes
candidate-source/bytecode fingerprint gates. This submission therefore makes
no claim that the repository-specific 24-vector verifier passed. The tests
here exercise the documented SSE framing behavior without network access.
