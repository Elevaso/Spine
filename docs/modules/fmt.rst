fmt
----
Formatting functions/classes

.. currentmodule:: src.spine

sub
^^^^^^^^

sub_value
~~~~~~~~~~
The :meth:`spine.fmt.sub.sub_value` function substitute placeholder patterns with values based on the provided dictionary of values. The placeholder pattern defaults to :code:`${NAME}` where :code:`NAME` is the placeholder name. If the variable type is a collection (list, set, tuple, dict) the function will call the :meth:`spine.itr.itr.iterate` function to check for the pattern within the collection.

Below is a simple example of how to use the :meth:`spine.fmt.sub.sub_value` function.

.. code-block:: python

    from spine.fmt import sub

    value = {
      "key1": [
        "No replacement",
        "${REPLACE_ME}",
        "No replacement"
      ],
      "key2": [
        "No replacement",
        "${REPLACE_ME_2}",
        "No replacement"
      ]
    }

    placeholder_values = {
      "REPLACE_ME": "I've been replaced",
      "REPLACE_ME_2": "I've also been replaced",
    }

    print(sub.sub_value(value, placeholder_values))

Running this could would produce following:

.. code-block:: json

    {
      "key1": [
        "No replacement",
        "I've been replaced",
        "No replacement"
      ],
      "key2": [
        "No replacement",
        "I've also been replaced",
        "No replacement"
      ]
    }

.. autofunction:: spine.fmt.sub.sub_value
