fobj
----
Functions/classes for working with file objects

.. currentmodule:: src.spine

find_obj
^^^^^^^^

find
~~~~~~~~~~
The :meth:`spine.fobj.find_obj.find` function will look for a specific file in the path provided and N parent directories where N is provided to the function.

For example, if your directory structure looks like the following

.. code-block:: text
   :linenos:

   .
   └── code                         # Main code directory
      └── applications              # Sub-directory for application code
        ├── config.json             # Configuration file for all applications
        └── test_app                # Test application
          └── app.py                # Main application file

In your :code:`app.py` you want to load configuration that is global to all other application directories. You create the file :code:`config.json` and store it in the applications sub-directory. You also want to add support for local projects overriding the global configuration.

The code to your :code:`app.py` would look like:

.. code-block:: python

    import json
    import os
    import spine

    def load_config():
      file_path = spine.fobj.find_obj.find(os.path.dirname(__file__), "config.json")

      if file_path is None:
        raise Exception("Configuration file not found!")
      else:
        with open(file_path, "r") as f:
          config = json.loads(f)

        return config

The :meth:`spine.fobj.find_obj.find` function would first check the base directory where :code:`app.py` exists (:code:`code/applications/test_app/`). If no :code:`config.json` file is found, it will move up one director and search in :code:`code/applications/`. It will repeat this process until a file is found or the number of :code:`search_dirs` has been reached.

.. autofunction:: spine.fobj.find_obj.find
