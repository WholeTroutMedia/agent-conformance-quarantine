import unittest
from candidate_submission import iter_sse_events, recount_grimm_khm001_frog_king_and_iron_henry_c35


class SSEConformanceTests(unittest.TestCase):
    def parse(self, chunks, ceiling=16369):
        return recount_grimm_khm001_frog_king_and_iron_henry_c35(chunks, ceiling)

    def test_basic_event(self):
        self.assertEqual(self.parse([b"data: hello\n\n"]), ["hello"])

    def test_utf8_split_across_chunks(self):
        wire = "data: \U0001f680\n\n".encode()
        self.assertEqual(self.parse([wire[:8], wire[8:10], wire[10:]]), ["\U0001f680"])

    def test_multiline_data(self):
        self.assertEqual(self.parse([b"data: first\ndata: second\n\n"]), ["first\nsecond"])

    def test_comments_and_non_data_fields(self):
        self.assertEqual(self.parse([b": ping\nevent: message\nid: 42\ndata: ok\n\n"]), ["ok"])

    def test_crlf_and_lone_cr(self):
        self.assertEqual(self.parse([b"data: a\r\n\rdata: b\r\r"]), ["a", "b"])

    def test_crlf_split_between_chunks(self):
        self.assertEqual(self.parse([b"data: x\r", b"\n\r", b"\n"]), ["x"])

    def test_bom(self):
        self.assertEqual(self.parse(["\ufeffdata: x\n\n".encode()]), ["x"])

    def test_empty_data_event(self):
        self.assertEqual(self.parse([b"data:\n\n"]), [""])

    def test_field_without_colon(self):
        self.assertEqual(self.parse([b"data\n\n"]), [""])

    def test_unterminated_event_discarded(self):
        self.assertEqual(self.parse([b"data: incomplete"]), [])

    def test_empty_chunks(self):
        self.assertEqual(self.parse([b"", b"data: x\n\n", b""]), ["x"])

    def test_exact_ceiling_accepted(self):
        self.assertEqual(self.parse([b"x" * 8], ceiling=8), [])

    def test_over_ceiling_rejected(self):
        with self.assertRaises(ValueError):
            self.parse([b"x" * 9], ceiling=8)

    def test_non_bytes_rejected(self):
        with self.assertRaises(TypeError):
            self.parse(["data: x\n\n"])

    def test_invalid_utf8_rejected(self):
        with self.assertRaises(UnicodeDecodeError):
            self.parse([b"data: \xff\n\n"])

    def test_nonpositive_ceiling_rejected(self):
        with self.assertRaises(ValueError):
            self.parse([], ceiling=0)

    def test_lazy_backpressure(self):
        requested = []
        def chunks():
            requested.append(1)
            yield b"data: first\n\n"
            requested.append(2)
            yield b"data: second\n\n"
        events = iter_sse_events(chunks())
        self.assertEqual(next(events), "first")
        self.assertEqual(requested, [1])
        self.assertEqual(next(events), "second")
        self.assertEqual(requested, [1, 2])


if __name__ == "__main__":
    unittest.main()
