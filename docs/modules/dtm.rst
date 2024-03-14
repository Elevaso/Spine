dtm
---
Date/time functions

.. currentmodule:: src.spine

now
^^^

utc_now
~~~~~~~
The :code:`utc_now` function allows you to get the current date & time in UTC with the time zone.

Below is an example snippet that prints the current time with timezone.

.. code-block:: python

    import spine

    print(spine.dtm.now.utc_now())


The output will look something like :code:`2024-03-13 18:50:09.252091+00:00`.

.. autofunction:: spine.dtm.now.utc_now
