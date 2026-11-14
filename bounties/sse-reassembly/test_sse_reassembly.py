import unittest

from sse_reassembly import parse_sse_chunks, recount_grimm_khm001_frog_king_and_iron_henry_c35


class SSEReassemblyTests(unittest.TestCase):
    def test_single_event(self):
        self.assertEqual(parse_sse_chunks([b"data: hello\n\n"]), ["hello"])

    def test_arbitrary_chunk_boundaries(self):
        wire = "data: caf\u00e9\r\n\r\n".encode()
        chunks = [wire[:8], wire[8:10], wire[10:]]
        self.assertEqual(parse_sse_chunks(chunks), ["caf\u00e9"])

    def test_multiline_data(self):
        self.assertEqual(parse_sse_chunks([b"data: one\ndata: two\n\n"]), ["one\ntwo"])

    def test_comments_and_other_fields(self):
        self.assertEqual(
            parse_sse_chunks([b": heartbeat\nevent: update\nid: 7\ndata: ok\n\n"]),
            ["ok"],
        )

    def test_crlf_split_between_chunks(self):
        self.assertEqual(parse_sse_chunks([b"data: x\r", b"\n\r", b"\n"]), ["x"])

    def test_bom(self):
        self.assertEqual(parse_sse_chunks(["\ufeffdata: x\n\n".encode()]), ["x"])

    def test_unterminated_event_is_not_dispatched(self):
        self.assertEqual(parse_sse_chunks([b"data: incomplete"]), [])

    def test_empty_data_event_is_not_dispatched(self):
        self.assertEqual(parse_sse_chunks([b"data:\n\n"]), [""])

    def test_invalid_utf8_fails_closed(self):
        with self.assertRaises(UnicodeDecodeError):
            parse_sse_chunks([b"data: \xff\n\n"])

    def test_chunk_limit(self):
        with self.assertRaises(ValueError):
            parse_sse_chunks([b"12345"], max_chunk_bytes=4)

    def test_compatibility_entrypoint(self):
        self.assertEqual(
            recount_grimm_khm001_frog_king_and_iron_henry_c35([b"data: x\n\n"]),
            ["x"],
        )


if __name__ == "__main__":
    unittest.main()
