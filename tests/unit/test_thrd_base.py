# pyright: reportMissingImports=false
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

# Python Standard Libraries
import queue
import time
import unittest

# 3rd Party Libraries


# Code Repository Sub-Packages
import context  # pylint: disable=unused-import
from spine.thrd import base


# pylint: disable=unused-argument
class MockThread(base.BaseThread):
    def test_init_function(self, **kwargs):
        pass

    def test_run_function(self, **kwargs):
        time.sleep(1)

    def test_del_function(self, **kwargs):
        pass

    init_func = test_init_function
    run_func = test_run_function
    stop_func = test_del_function


# pylint: disable=unused-argument
class MockFailureOnRunThread(base.BaseThread):
    def test_init_function(self, **kwargs):
        pass

    def test_run_function(self, **kwargs):
        raise AttributeError("Test Exception")

    def test_del_function(self, **kwargs):
        pass

    init_func = test_init_function
    run_func = test_run_function
    stop_func = test_del_function


class MockFailureOnDelThread(base.BaseThread):
    def test_run_function(self, **kwargs):
        time.sleep(1)

    def test_del_function(self, **kwargs):
        raise ValueError("Test Exception")

    run_func = test_run_function
    stop_func = test_del_function


class TestBaseThread(unittest.TestCase):
    def create_threads(
        self,
        thread_class: object,
        threads: int = 1,
        thread_queue: queue.Queue = None,
        params: dict = None,
    ) -> list:
        params = params or {}
        thread_list = []

        class_name = thread_class.__name__

        for x in range(threads):
            if thread_queue:
                thread = thread_class(
                    worker_queue=thread_queue, thread_num=x, **params
                )
            else:
                thread = thread_class(thread_num=x, **params)

            thread.name = class_name + str(x)

            thread.daemon = True
            thread_list.append(thread)
            thread.start()

        return thread_list

    def test_basic(self):
        thread_list = self.create_threads(MockThread)

        _ = [t.join() for t in thread_list]

    def test_queue(self):
        thread_queue = queue.Queue()
        thread_queue.put({"test": "value"})

        thread_list = self.create_threads(
            MockThread, 2, thread_queue=thread_queue
        )

        thread_queue.join()

        rows_processsed = sum([t.rows_processed for t in thread_list])

        self.assertEqual(rows_processsed, 1)

    def test_queue_error(self):
        thread_queue = queue.Queue()
        thread_queue.put({"test": "value"})

        with self.assertLogs(level="ERROR") as log:
            thread_list = self.create_threads(
                MockFailureOnRunThread, 2, thread_queue=thread_queue
            )

            thread_queue.join()

        rows_processsed = sum([t.rows_processed for t in thread_list])
        rows_errored = sum([t.rows_errored for t in thread_list])

        self.assertIn("Error processing record", log.output[0])

        self.assertEqual(rows_processsed, 0)
        self.assertEqual(rows_errored, 1)

    def test_invalid_thread_num(self):
        thread_list = self.create_threads(MockFailureOnDelThread)

        _ = [t.join() for t in thread_list]

        with self.assertLogs(level="WARNING") as log:
            del thread_list[0]

        self.assertIn(
            "Error while terminating worker thread MockFailureOnDelThread0",
            log.output[0],
        )

    def test_no_run_func(self):
        with self.assertLogs(level="ERROR") as log:
            _ = self.create_threads(base.BaseThread, 1)

        self.assertIn("Unable to run thread, no function found", log.output[0])


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
