log
----
Logging functions and classes

.. note::

    Best practices retrieved from `Python Logging Cookbook <https://docs.python.org/3/howto/logging-cookbook.html>`_

.. currentmodule:: src.spine

append
^^^^^^

LogAppend
~~~~~~~~~
A custom class (sub-class of LogAdapter) is also included in the log module to provide an option to automatically append data to every log message (e.g. a Session Id, Username of the executor).

This is normally done through a :meth:`logging.LogAdapter`, however, it uses the extra keyword argument and if the LogAdapter and the individual logging call with extra keyword argument is provided, the results are not combined. This custom class allows for merging of the two.

To use the custom class, add the following (usually after initial setting of logging settings at initialization):

.. code-block::

    from spine.log import append

    user = "me"
    
    LOGGER = append.LogAppend(LOGGER, {'user': user, 'session_id': 'testing session id'})

Now, every logging message will contain a :code:`user` and :code:`session_id` key with the values provided to the LogAppend class

.. autoclass:: spine.log.append.LogAppend
    :special-members: __init__

config
^^^^^^

setup
~~~~~
The :meth:`spine.log.config.setup` provides a quick way to configure logging through Python code or a JSON file.

Default Config
""""""""""""""
Spine includes default log configuration files located in :code:`spine/log/data` and can easily be referenced through their short name in Python code.

Below is an example of how to use the default configuration for JSON logging.

.. code-block:: python

    from spine.log import config

    config.setup(log_format="json")

Optionally, you can override the default log configuration level by providing the :code:`log_level` argument.

.. code-block:: python

    from spine.log import config

    config.setup(log_format="json", log_level="WARN")

Custom Config
"""""""""""""
To use your own log config file in your project, create a :code:`.json` file that resembles the following:

.. code-block:: JSON
    :linenos:
    :emphasize-lines: 6-11,18

    {
        "version": 1,
        "disable_existing_loggers": false,
        "formatters": {
            "json":{
                "include_keys":["message", "module", "levelname", "name", "funcName", "asctime", "thread", "threadName"], 
                "()":"spine.log.fmt_json.JsonFormatter",
                "timestamp_key": "timestamp",
                "session_key":"init_id",
                "timezone":"US/Central",
                "dtm_format": "%Y-%m-%d %H:%M:%S %Z"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "json",
                "stream": "ext://sys.stdout"
            }
        },
            "root": {
            "level": "INFO",
            "handlers": ["console"],
            "propogate":"no"
        }
    }

In your python code, when calling the :meth:`spine.log.config.setup` function, provide the path to the :code:`.json` file in your project.

.. code-block:: python

    import os
    from spine.log import config

    config.setup(path=os.path.join(os.path.dirname(__file__), "log.json"))

Python Config - Functions
"""""""""""""""""""""""""
If you would rather setup logging without a configuration file, you can set this up directly in your Python code.

.. code-block:: python
    :linenos:
    :emphasize-lines: 11,14

    import logging
    from spine.log import append, fmt_json

    LOGGER = logging.getLogger(__name__)

    LOGGER.setLevel(logging.DEBUG)
    log_handler = logging.StreamHandler()
    LOGGER.addHandler(log_handler)

    # Create a JSON Formatter instance
    formatter = fmt_json.JsonFormatter()

    # Add JSON Formatter to Log Handler
    log_handler.setFormatter(formatter)

Optional arguments can be provided to the :code:`Formatter` class. See :meth:`spine.log.fmt.BaseFormatter` for options.

Python Config - Dictionary
""""""""""""""""""""""""""
Another method of setting the configuration directly in Python is to use a :code:`dict`.

.. code-block:: python
   :linenos:
   :emphasize-lines: 4, 10, 34

    import logging
    import logging.config

    log_config = {
        "version": 1,
        "disable_existing_loggers": false,
        "formatters": {
            "json":{
                "include_keys":["message", "module", "levelname", "name", "funcName", "asctime", "thread", "threadName"], 
                "()":"spine.log.fmt_json.JsonFormatter",
                "timestamp_key": "timestamp",
                "session_key":"init_id",
                "timezone":"US/Central",
                "dtm_format": "%Y-%m-%d %H:%M:%S %Z"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "json",
                "stream": "ext://sys.stdout"
            }
        },
            "root": {
            "level": "INFO",
            "handlers": ["console"],
            "propogate":"no"
        }
    }

    LOGGER = logging.getLogger(__name__)

    logging.config.dictConfig(log_config)

.. autofunction:: spine.log.config.setup

fmt
^^^^^^^^

BaseFormatter
~~~~~~~~~~~~~~
The :meth:`spine.log.fmt.BaseFormatter` class provides the foundational functions for other log formatters. It includes:

1. Date/time formatting
2. Timezone support (defaults to UTC)
3. Support for the :code:`extra` keyword argument support

.. code-block::

   LOGGER.info('testing', extra={'test1': 'hello', 'test2': 'there'})

4. Session identifier (defaults to UUID if none provided) 

.. autoclass:: spine.log.fmt.BaseFormatter
    :special-members: __init__

fmt_json
^^^^^^^^

JsonFormatter
~~~~~~~~~~~~~~
The :meth:`spine.log.fmt_json.JsonFormatter` inherits from the :meth:`spine.log.fmt.BaseFormatter` but provides an output function to convert logs into JSON format.

Using the default JSON logging configuration file and setup from `Default Config`_ and running the following code

.. code-block::

   LOGGER.info('test')

will output something like:

.. code-block:: JSON
   :linenos:

   {"name": "root", "msg": "test", "args": [], "levelname": "INFO", "levelno": 20, , "filename": "log.py", "module": "log", "exc_info": null, "exc_text": null, "stack_info": null, "lineno": 211, "funcName": "<module>", "created": 1575907675.176455, "msecs": 176.45502090454102, "relativeCreated": 1.3270378112792969, "thread": 4610047424, "threadName": "MainThread", "processName": "MainProcess", "process": 62034, "message": "test", "asctime": "2019-12-09 16:07:55.176455 +0000"}

To add additional key/value pairs, you can use the :code:`extra` keyword argument in the logger:

.. code-block::

   LOGGER.info('testing', extra={'test1': 'hello', 'test2': 'there'})

or provide the raw JSON/dictionary object type to the logger:

.. code-block::

   LOGGER.info({'test1': 'hello', 'test2': 'there'})

.. note::

    The only difference between the two methods is that the first contains a msg key (with the value of testing) whereas the second does not (since the message was only the contents of the extra keyword arguments).

    The other difference is that if you decided to not format the output in Json format (e.g. using a standard CLI print type format), the extra keyword arguments are not automatically printed to the console, so only the values in the message (in the first usage example) will be shown. For example:

    .. code-block::

        import logging

        logging.basicConfig(
            level=logging.DEBUG,
            format="...%(asctime)s...%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        LOGGER.info({'test1': 'hello', 'test2': 'there'})
        LOGGER.info('testing', extra={'test1': 'hello', 'test2': 'there'})

    will output:

    .. code-block:: bash
        :linenos:

        ...2019-12-09 10:21:50...{'test1': 'hello', 'test2': 'there'}
        ...2019-12-09 10:21:50...testing

    This problem can be overcome by using the formatter_standard.StandardFormatter class, which is intended for terminal output, but will include an extra keyword arguments in a standard format

.. autoclass:: spine.log.fmt_json.JsonFormatter

fmt_standard
^^^^^^^^^^^^

StandardFormatter
~~~~~~~~~~~~~~~~~
The :meth:`spine.log.fmt_standard.StandardFormatter` inherits from the :meth:`spine.log.fmt.BaseFormatter` but provides an output function to convert logs in standard (i.e. Command Line Interface) format.

.. autoclass:: spine.log.fmt_standard.StandardFormatter
