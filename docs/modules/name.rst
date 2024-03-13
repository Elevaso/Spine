*********
name
*********
# TODO Add sub-module description

# TODO Add name of sub-module directory
.. currentmodule:: src.name

# TODO Update section with additional details for each function/class similar to the below
now
========

utc_now
---------

The :code:`utc_now` function allows you to get the current date & time in UTC with the time zone.

.. autofunction:: rau_spine.dtm.now.utc_now

split
========

split_time
----------
Split an integer or float into days, hours, minutes, seconds, milliseconds

.. code-block::

   from rau_spine.dtm.split import split_time

   print(split_time(
    120
   ))

The above code will print a Tuple of values :code:`(00, 00, 02, 00, 000000)`

.. autofunction:: rau_spine.dtm.split.split_time
