# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import context
import queue
import time
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
from spine.thrd import mgr
from test_thrd_base import MockThread, MockFailureOnRunThread


class TestCreate(unittest.TestCase):
    def create_threads(
        self, num: int = 1, thread_queue: queue.Queue = None
    ) -> list:
        return mgr.create(num, MockThread, {"target": ""}, thread_queue)

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
        thread_queue = queue.Queue()

        thread_queue.put({"test": "data"})

        thread_list = self.create_threads(2, thread_queue=thread_queue)

        thread_queue.join()

        self.assertEqual(sum([t.rows_processed for t in thread_list]), 1)


class TestHasWorkingThread(unittest.TestCase):
    def setUp(self):
        self.stop_threads = False

    def create_threads(self, num: int = 1, q: queue.Queue = None) -> list:
        return mgr.create(num, MockThread, {"target": ""}, q)

    def run_thread(self):
        while True:
            if self.stop_threads:
                break

    def test_has_active(self):
        thread_list = self.create_threads()

        time.sleep(0.1)

        output = mgr.has_working_thread(thread_list)

        self.stop_threads = True

        _ = [t.join() for t in thread_list]

        self.assertTrue(output)

    def test_has_no_active(self):
        thread_list = self.create_threads()

        time.sleep(0.1)

        self.stop_threads = True

        _ = [t.join() for t in thread_list]

        output = mgr.has_working_thread(thread_list)

        self.assertFalse(output)

    def test_empty_thread_list(self):
        thread_list = []

        output = mgr.has_working_thread(thread_list)

        self.assertFalse(output)


class TestThreadMetrics(unittest.TestCase):
    def create_threads(
        self, num: int = 1, thread_queue: queue.Queue = None
    ) -> list:
        return mgr.create(num, MockThread, {"target": ""}, thread_queue)

    def test_success(self):
        thread_queue = queue.Queue()

        thread_queue.put({"test": "data"})

        thread_list = self.create_threads(2, thread_queue=thread_queue)

        thread_queue.join()

        self.assertTupleEqual(mgr.thread_metrics(thread_list), (1, 0, 2))

    def test_errored(self):
        thread_queue = queue.Queue()

        thread_queue.put({"test": "data"})

        with self.assertLogs(level="ERROR") as log:
            thread_list = mgr.create(
                2, MockFailureOnRunThread, {"target": ""}, thread_queue
            )

        thread_queue.join()

        self.assertTupleEqual(mgr.thread_metrics(thread_list), (0, 1, 2))


class TestWaitQueueEmpty(unittest.TestCase):
    def create_threads(
        self, num: int = 1, thread_queue: queue.Queue = None
    ) -> list:
        return mgr.create(
            num, MockThread, {"target": ""}, thread_queue=thread_queue
        )

    def put_in_queue(self, thread_queue: queue.Queue, num: int = 1):
        for _ in range(num):
            thread_queue.put({"test": "hello"})

    def test_queue(self):
        thread_queue = queue.Queue()
        self.put_in_queue(thread_queue)

        thread_list = self.create_threads(thread_queue=thread_queue)

        mgr.wait_queue_empty(thread_queue, thread_list, interval=1)

        output = [t.rows_processed for t in thread_list]

        self.assertEqual(output[0], 1)

    def test_run_func_error(self):
        thread_queue = queue.Queue()
        self.put_in_queue(thread_queue)

        with self.assertLogs(level="ERROR") as log:
            thread_list = mgr.create(
                1,
                MockFailureOnRunThread,
                {"target": ""},
                thread_queue=thread_queue,
            )

        mgr.wait_queue_empty(thread_queue, thread_list, interval=1)

        output = [t.rows_errored for t in thread_list]

        self.assertIn("Error processing record", log.output[0])

        self.assertEqual(output[0], 1)

    def test_records_in_queue(self):
        thread_queue = queue.Queue()
        self.put_in_queue(thread_queue)

        thread_list = self.create_threads()

        with self.assertRaises(Exception) as cm:
            mgr.wait_queue_empty(thread_queue, thread_list, interval=1)

        self.assertEqual(
            "1 records in queue with no active threads",
            str(cm.exception),
        )

    def test_empty_queue(self):
        thread_queue = queue.Queue()

        thread_list = self.create_threads(thread_queue=thread_queue)

        mgr.wait_queue_empty(thread_queue, thread_list, interval=1)

        output = [t.rows_processed for t in thread_list]

        self.assertEqual(sum(output), 0)

    def test_interval(self):
        thread_queue = queue.Queue()
        self.put_in_queue(thread_queue, 6)

        thread_list = self.create_threads(2, thread_queue=thread_queue)

        with self.assertLogs(level="INFO") as log:
            mgr.wait_queue_empty(thread_queue, thread_list, interval=1)

        output = [t.rows_processed for t in thread_list]

        self.assertEqual(sum(output), 6)
        self.assertIn("Records in Queue", log.output[0])


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
