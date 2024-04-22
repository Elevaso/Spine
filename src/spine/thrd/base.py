"""
.. module:: base
    :platform: Unix, Windows
    :synopsis: Base threading class
"""

# Python Standard Libraries
import logging
import threading

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


class BaseThread(threading.Thread):
    """Base multi-threading class with built-in functions"""

    init_func = None
    run_func = None
    stop_func = None

    def __init__(self, thread_num: int, **kwargs):
        """Initialize a worker thread

        Args:
            thread_num (int): The unique number for the thread

        Kwargs:
            worker_queue (queue.Queue): Queue to pull work from,
            defaults to None

            .. note::

                Additional kwargs provided to the class will be
                stored in the kwargs property of the class.
        """
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

        self.name = "-".join([self.__class__.__name__, str(thread_num)])
        self.thread_num = thread_num
        self.queue = kwargs.pop("worker_queue", None)

        self.kwargs = kwargs

        self.rows_processed = 0
        self.rows_errored = 0

        if self.init_func:
            self.init_func(**kwargs)

        LOGGER.debug(
            f"Initialized {self.name} thread",
        )

    def run(self):
        """Function to run the thread for processing"""
        if self.run_func:
            if self.queue:
                self.process_queue()
            else:
                self.run_func()
        else:
            LOGGER.error(
                "Unable to run thread, no function found",
                extra={"thread_name": self.name},
            )

    def process_queue(self):
        """Process a record from shared queue if provided during
        initialization
        """
        while True:
            try:
                record = self.queue.get()

                self.run_func(**record)

                self.rows_processed += 1
            except Exception as e:
                self.rows_errored += 1

                LOGGER.error(
                    "Error processing record",
                    exc_info=True,
                    extra={
                        "error": str(e),
                        **record,
                        "thread_name": self.name,
                    },
                )

            self.queue.task_done()

            LOGGER.debug(
                f"Processed row",
                extra={"thread_name": self.name},
            )

    def __del__(self):
        """De-initialize the class calling stop_func if required"""
        if self.stop_func:
            LOGGER.debug(f"De-initializing thread {self.name}")
            try:
                self.stop_func()
            except Exception as e:
                LOGGER.warning(
                    f"Error while terminating worker thread {self.name}",
                    exc_info=True,
                    extra={"error": str(e), "thread_name": self.name},
                )
