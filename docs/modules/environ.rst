environ
-------
Environment & environment variable functions

.. currentmodule:: src.spine

load
^^^^^

load_env
~~~~~~~~
The :meth:`spine.environ.load.load_env` function finds a :code:`.env` file and loads the values into environment variables. This is helpful if you have multiple values for different environments that you want to test against.

For example, you have have a :code:`dev.env` and :code:`test.env`. When you call the :meth:`spine.environ.load.load_env` function you pass in the prefix which will load one of the two files.

By default, the function will look for :code:`.env` file within 4 directories of the current project file calling :meth:`spine.environ.load.load_env`.

.. autofunction:: spine.environ.load.load_env

var
^^^

get_var
~~~~~~~~
The :meth:`spine.environ.var.get_var` function retrieves an environment variable or returns a default value if not found.

.. autofunction:: spine.environ.var.get_var

set_var
~~~~~~~
The :meth:`spine.environ.var.set_var` function creates or modifies an environment variable. It also provides the option to prevent overwrites or mocking the change.

.. autofunction:: spine.environ.var.set_var
