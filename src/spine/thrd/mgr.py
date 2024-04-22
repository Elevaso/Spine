"""
.. module:: mgr
    :platform: Unix, Windows
    :synopsis: Function to manage threads
"""

# Python Standard Libraries
import logging
import queue
import time

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def create(
    threads: int, thread_class: object, params: dict, q: queue.Queue = None
) -> list:
    """Create threads for parallel processing

    Args:
        threads (int): Number of threads to create

        thread_class (object): Thread class to create

        params (dict): Dictionary of parameters to pass into thread

        q (queue.Queue, Optional): Queue to retrieve items to work,
        defaults to None

    Raises:
        ValueError if threads == 0

    Returns:
        list: List of thread objects created
    """
    if threads == 0:
        raise ValueError("Threads must be greater than 0")

    thread_list = []

    class_name = thread_class.__name__

    for x in range(threads):
        LOGGER.debug(f"Creating {class_name} thread {x}")

        if q:
            thread = thread_class(worker_queue=q, thread_num=x, **params)
        else:
            thread = thread_class(thread_num=x, **params)

        thread.name = class_name + str(x)

        thread.daemon = True
        thread_list.append(thread)
        thread.start()

    LOGGER.info(f"Created {len(thread_list)} {class_name} thread(s)")

    return thread_list


def has_working_thread(thread_list: list) -> bool:
    """Checks if there are threads still alive

    Args:
        thread_list (list): List of thread objects

    Returns:
        bool: True/False if has at least one thread alive
    """
    for t in thread_list:
        if t.is_alive():
            return True

    return False


def thread_metrics(thread_list: list) -> tuple[int, int, int]:
    """Retrieves built-in metrics from all threads

    Args:
        thread_list (list): List of thread objects

    Returns:
        tuple: Containing
            rows_processed: Number of queue records processed for all threads
            rows_errored: Number of queue records errored for all threads
            threads: Number of threads
    """
    return (
        sum([t.rows_processed for t in thread_list]),
        sum([t.rows_errored for t in thread_list]),
        len(thread_list),
    )


def wait_queue_empty(q: queue.Queue, thread_list: list, interval: int = 5):
    """Check if a queue is empty and outputs logging messages, additionally
    checks if there are threads alive to prevent waiting for a queue to finish
    if all worker threads have stopped

    Args:
        q (queue.Queue): Queue to check for empty status

        thread_list (list): List of threads working the queue

        interval (int, Optional): Interval in seconds to print queue depth,
        defaults to 5

        .. note::

            If set to 0, the queue will not be actively checked while printing
            status message, instead it will wait until the queue is empty
            through the queue.join() function

    Raises:
        Exception: If queue is not empty and no working threads in thread_list
    """
    if interval > 0:
        __wait(q, thread_list, interval)

    q.join()


def __wait(q: queue.Queue, thread_list: list, interval: int = 5):
    """Loop until queue is empty

    Args:
        q (queue.Queue): Queue to check for empty status

        thread_list (list): List of threads working the queue

        interval (int, Optional): Interval in seconds to print queue depth,
        defaults to 5

        .. note::

            If set to 0, the queue will not be actively checked while printing
            status message, instead it will wait until the queue is empty
            through the queue.join() function

    Raises:
        Exception: If queue is not empty and no working threads in thread_list
    """
    i = 0

    while not q.empty():
        time.sleep(1)

        if has_working_thread(thread_list):
            i += 1

            __log_size(i, interval, q.qsize())
        else:
            raise Exception(
                f"{q.qsize()} records in queue with no active threads"
            )


def __log_size(i: int, interval: int, q_size: int):
    """Log the current size of queue if interval matches

    Args:
        i (int): Current second

        interval (int): Interval at which to print

        q_size (int): Current queue size
    """
    if i == interval:
        LOGGER.info(f"{q_size} Records in Queue")
        i = 0
