app
---
Functions/classes for application specific usage

.. currentmodule:: src.spine

caller
^^^^^^

get_caller
~~~~~~~~~~
The :meth:`spine.app.caller.get_caller` function retrieves the root code file and path. This is helpful if you have an application that references nested modules and you need to know the initiating code path.

For example, you create a python module named :code:`json_logger` that can be used by multiple python applications/scripts. You create a file called :code:`log_setup.py` with code checks for a file named :code:`log_config.json` stored at the application root directory. The module code looks like:

.. code-block:: python

    import json
    import os
    import spine

    def setup():
      _, path = spine.app.caller.get_caller() # Get the path of the calling file
      
      log_config_path = os.path.join(path, "log_config.json")

      if os.path.exists(log_config_path): # Check if file exists at application path
        print(f"File found at {log_config_path}")
        with open(log_config_path, "r") as f: # Read file
            log_config = json.loads(f) # Load to variable
      else:
        print(f"No file found at {log_config_path}")
        log_config = {}
    
      return log_config

Next you create a python directory called :code:`test_app` with a file called :code:`app.py` with the following code:

.. code-block:: python

    import json_logger

    json_logger.setup()

The directory structure would look like this (assuming it's in your :code:`~/code/` directory):

.. code-block:: text
   :linenos:

   .
   ├── json_logger                  # json_logger Python module
      └── log_setup.py              # Setup logging
   └── test_app                     # Application code
      └── app.py                    # Main application file

If you ran the code as-is, it would print :code:`No file found at ~/code/test_app/`.

If you add a file to the :code:`test_app` directory called :code:`log_config.json`, the directory structure would look like:

.. code-block:: text
   :linenos:

   .
   ├── json_logger                  # json_logger Python module
      └── log_setup.py              # Setup logging
   └── test_app                     # Application code
      ├── app.py                    # Main application file
      └── log_config.json           # Configuration Json file for logging

Running the code now would print :code:`File found at ~/code/test_app/`.

.. autofunction:: spine.app.caller.get_caller
