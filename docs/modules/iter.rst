iter
----
Iteration functions

.. currentmodule:: src.spine

iter
^^^^^^^^

iterate
~~~~~~~~~~
The :meth:`spine.iter.iter.iterate` function loops through collections (list, dict, tuple, set) and executes the provided function on non-collection data types. The :meth:`spine.iter.iter.iterate` function is used by :meth:`spine.fmt.sub.sub_value` to perform string replacements.

Another use case would be to convert data types, for example, if you want to change all integers into string with zero padding.

.. code-block:: python

    from spine.iter import iter

    def convert(val: int) -> str:
      return val.zfill(4)

    value = [
      {
        "name": "Test1",
        "count": 1
      },
      { 
        "name": "Test2",
        "count": 10
      } 
    ]

    print(iter.iterate(val=value, custom_type_map={int: convert}))

The above could would iterate through the list of dictionary items and change the count to zero pad with 4 characters in total. The output would be:

.. code-block:: JSON

    [
        {
            "name": "Test1",
            "count": "0001"
        },
        {
            "name": "Test2",
            "count": "0010",
        }
    ]

.. autofunction:: spine.iter.iter.iterate
