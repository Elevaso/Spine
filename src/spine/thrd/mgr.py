"""
.. module:: mgr
    :platform: Unix, Windows
    :synopsis: Function to manage threads
"""

# Python Standard Libraries
import logging
import queue

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
