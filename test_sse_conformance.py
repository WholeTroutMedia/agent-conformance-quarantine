import unittest
from candidate_submission import iter_sse_events, recount_grimm_khm001_frog_king_and_iron_henry_c35


class SSEConformanceTests(unittest.TestCase):
    def parse(self, chunks, ceiling=16369):
        return recount_grimm_khm001_frog_king_and_iron_henry_c35(chunks, ceiling)

    def test_24_independent_vectors(self):
        vectors = [
            ([b"data: hello\n\n"], ["hello"]),
            ([b'data: {"method":"ping"}\n\n'], ['{"method":"ping"}']),
            ([b"data: \xc2", b"\xb5s\n\n"], ["µs"]),
            ([b"data: \xe2\x82", b"\xac\n\n"], ["€"]),
            ([b"data: \xf0\x9f", b"\x9a\x80\n\n"], ["🚀"]),
            ([b"data: x\r\n\r\n"], ["x"]),
            ([b": keepalive\ndata: ok\n\n"], ["ok"]),
            ([b"data: first\ndata: second\n\n"], ["first\nsecond"]),
            ([b"data: a\r\r"], ["a"]),
            ([b"data: a\r\n\rdata: b\n\n"], ["a", "b"]),
            (["\ufeffdata: bom\n\n".encode("utf-8")], ["bom"]),
            ([b"data:\n\n"], [""]),
            ([b"data\n\n"], [""]),
            ([b"data: unfinished"], []),
            ([b"", b"data: x\n\n", b""], ["x"]),
            ([b"data: 1\n\ndata: 2\n\n"], ["1", "2"]),
            ([b"data:  two\n\n"], [" two"]),
            ([b"event: update\nid: 7\nretry: 1000\n\n"], []),
            ([b": heartbeat\n\n"], []),
            ([b"data: split-crlf\r", b"\n\r", b"\n"], ["split-crlf"]),
            ([b"data: a:b\n\n"], ["a:b"]),
            ([b"data: kept\n\n\n"], ["kept"]),
            ([b"data: \xff\n\n"], UnicodeDecodeError),
            ([b"x" * 8], []),
        ]
        for index, (chunks, expected) in enumerate(vectors, 1):
            with self.subTest(vector=index):
                if isinstance(expected, type) and issubclass(expected, Exception):
                    with self.assertRaises(expected):
                        self.parse(chunks)
                else:
                    self.assertEqual(self.parse(chunks), expected)

    def test_chunk_ceiling(self):
        self.assertEqual(self.parse([b"x" * 8], ceiling=8), [])
        with self.assertRaises(ValueError):
            self.parse([b"x" * 9], ceiling=8)

    def test_rejects_non_bytes(self):
        with self.assertRaises(TypeError):
            self.parse(["data: x\n\n"])

    def test_rejects_invalid_ceiling(self):
        with self.assertRaises(ValueError):
            self.parse([], ceiling=0)
        with self.assertRaises(TypeError):
            self.parse([], ceiling=True)

    def test_lazy_backpressure(self):
        consumed = []
        def chunks():
            consumed.append("first")
            yield b"data: one\n\n"
            consumed.append("second")
            yield b"data: two\n\n"
        events = iter_sse_events(chunks())
        self.assertEqual(next(events), "one")
        self.assertEqual(consumed, ["first"])
        self.assertEqual(next(events), "two")
        self.assertEqual(consumed, ["first", "second"])


if __name__ == "__main__":
    unittest.main()
