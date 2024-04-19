# pyright: reportMissingImports=false

# Python Standard Libraries
import context
import queue
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.thrd import mgr
from test_thrd_base import MockThread


class TestCreateThreads(unittest.TestCase):
    def create_threads(self, num: int = 1, q: queue.Queue = None) -> list:
        return mgr.create(num, MockThread, {"target": ""}, q)

    def test_invalid_thread_num(self):
        with self.assertRaises(ValueError) as cm:
            _ = self.create_threads(0)

        self.assertEqual(
            "Threads must be greater than 0",
            str(cm.exception),
        )

    def test_basic(self):
        with self.assertLogs(level="INFO") as log:
            thread_list = self.create_threads(2)

        _ = [t.join() for t in thread_list]

        self.assertIn("Created 2 MockThread thread(s)", log.output[0])

    def test_queue(self):
        q = queue.Queue()

        q.put({"test": "data"})

        thread_list = self.create_threads(2, q=q)

        q.join()

        self.assertEqual(sum([t.rows_processed for t in thread_list]), 1)


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
