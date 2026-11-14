# Independent SSE implementation and test record

This branch contains a standalone implementation of the original SSE parsing
requirement and a hermetic 24-vector test suite.

Coverage includes incremental UTF-8 decoding, arbitrary chunk boundaries,
LF/CRLF/lone-CR delimiters, BOM handling, multiline data, comments and ignored
fields, empty data events, incomplete-event handling, chunk ceilings, invalid
UTF-8 rejection, and lazy iterator backpressure.

Run the independent tests with:

```sh
python3 -m unittest -v
```

The repository's `verify_conformance.py` was not executed. Static inspection
shows that it performs network requests to a hard-coded plaintext-HTTP host
and includes environment/fingerprint checks. This branch therefore makes no
claim that the repository-specific escrow verifier passes or that any escrow
is funded or payable.
