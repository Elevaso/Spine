calc
----
Functions/classes for various calculations

.. currentmodule:: src.spine

hsh
^^^

hash_content
~~~~~~~~~~~~
The :meth:`spine.calc.hsh.hash_content` function provides an easy way to hash content by providing the object and it will perform necessary actions in advance (i.e. unzip an archive file to hash all file contents, convert dictionary or lists to JSON string).

.. autofunction:: spine.calc.hsh.hash_content

hash_file
~~~~~~~~~
The :meth:`spine.calc.hsh.hash_file` function calulates a single file object hash. If the file is large, it will be performed in blocks.

.. autofunction:: spine.calc.hsh.hash_file

hash_string
~~~~~~~~~~~
The :meth:`spine.calc.hsh.hash_string` function calulates the hash of the provided string.

.. autofunction:: spine.calc.hsh.hash_string
