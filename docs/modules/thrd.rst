thrd
----
Functions/classes for multi-threading

.. currentmodule:: src.spine

base
^^^^^^

BaseThread
~~~~~~~~~~
The :meth:`spine.thrd.base.BaseThread` class provides a base threading class with built-in functions for initializing, running, and de-initializing multiple threads.

For example, if you need to connect to a database during thread initialization, then process records from a queue, and ensure proper database disconnection when complete, your code would look like:

.. code-block:: python

    from spine.thrd.base import BaseThread

    class DBThread(BaseThread):
        def connect(self, **kwargs):
            # Database connection code goes here
            print(kwargs["db_user"], kwargs["db_pwd"], kwargs["db_instance"])
            pass
        
        def disconnect(self):
            # Database disconnection code goes here

        init_func = self.connect
        stop_func = self.disconnect

The corresponding code to use the DBThread class above would look like:

.. code-block:: python

    import queue

    q = queue.Queue() # Python shared queue between threads

    q.put({"test": "value"}) # Insert values into the queue

    thread_list = []

    for x in range(10):
        thread = DBThread(worker_queue=q, thread_num=x, db_user="name", db_pwd="password", db_instance="test.example")

        thread.name = DBThread.__name__ + str(x)

        thread.daemon = thread_num
        thread_list.append(thread)
        thread.start()
    
    q.join() # Wait until all queue ites have been processed

    # Print stats from the threads
    print("Procesed records: " + sum([t.rows_processed for t in thread_list]))
    print("Errored records: " + sum([t.rows_errored for t in thread_list]))

.. autoclass:: spine.thrd.base.BaseThread
    :special-members: __init__

mgr
^^^^^^

create
~~~~~~~~~~
The :meth:`spine.thrd.mgr.create` function will generate X number of threads based on the class and number requested. Optionally, you can pass in additional parameters for the thread initialization (such as credentials to establish separate database connections) and shared python queue.

A basic example looks like:

.. code-block:: python

    from spine.thrd.base import BaseThread
    from spine.thrd.mgr import create


    thread_list = create(10, BaseThread)

    _ = [t.join() for t in thread_list] # Wait until all threads are finished running

An example using python queue looks like:

.. code-block:: python

    import queue
    from spine.thrd.base import BaseThread
    from spine.thrd.mgr import create

    q = queue.Queue()
    q.put({"test": "data"})

    thread_list = create(10, BaseThread, q=q)

    q.join() # Wait until queue is empty

    # Print the number of queue records processed or errored
    print(sum([t.rows_processed for t in thread_list]))
    print(sum([t.rows_errored for t in thread_list]))

.. autofunction:: spine.thrd.mgr.create

has_working_thread
~~~~~~~~~~~~~~~~~~
The :meth:`spine.thrd.mgr.has_working_thread` function checks all threads provided and returns True if any are active, or False if none are active.

.. autofunction:: spine.thrd.mgr.has_working_thread

thread_metrics
~~~~~~~~~~~~~~~~~~
The :meth:`spine.thrd.mgr.thread_metrics` function calculates metrics from the threads.

.. autofunction:: spine.thrd.mgr.thread_metrics

wait_queue_empty
~~~~~~~~~~~~~~~~~~
The :meth:`spine.thrd.mgr.wait_queue_empty` function checks a shared queue until all items have been processed or there are no active threads, periodically logging the estimated size of the queue.

Example code:

.. code-block:: python

    import queue
    from spine.thrd.base import BaseThread
    from spine.thrd.mgr import create, thread_metrics, wait_queue_empty

    q = queue.Queue()
    q.put({"test": "data"})

    thread_list = create(10, BaseThread, q=q)

    wait_queue_empty(q, thread_list)

    # Print the number of queue records processed or errored
    print(thread_metrics(thread_list))

.. autofunction:: spine.thrd.mgr.wait_queue_empty
