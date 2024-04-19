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

        init_func = connect
        stop_func = disconnect

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
