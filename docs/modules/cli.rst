cli
---
Command Line Interface (CLI) functions

.. currentmodule:: src.spine

args
^^^^

args_to_dict
~~~~~~~~~~~~
The :meth:`spine.cli.args.args_to_dict` function converts arguments to a dictionary object instead of :meth:`argparse.Namespace`. This is useful if you want to add custom logic for adding default values, overriding, or removing arguments before sending to additional functions.

.. autofunction:: spine.cli.args.args_to_dict

exc
^^^^

main
~~~~~~~~~~~~
The :meth:`spine.cli.exc.main` provides an easy function for setting up and executing your command line interface program. You provide the path to the configuration file as documented in `build`_ and a dictionary of possible functions to execute.

Using the JSON file in `build`_, and creating your main CLI file similar to:

.. code-block:: python

    from spine.cli.exc import main

    def list_config(**kwargs):
        print("Listing config")
        print(f"Kwargs: {kwargs}")

    def add_config(**kwargs):
        print("Adding config")
        print(f"Kwargs: {kwargs}")

    main("argparse.json", {
        "list_config": list_config,
        "add_config": add_config
    })

You can easily run your CLI program :code:`<name>.py --help`. To validate the functions are being executed, run :code:`<name>.py config list` to output something like:

.. code-block:: shell

    Listing config
    Kwargs: {'quiet': False, 'verbose': False, 'func': 'list_config'}

.. note::

    The func_map key and value do not need to match. For example, the above code could look like:

    .. code-block:: python

        from spine.cli.exc import main

        def list_configuration(**kwargs):
            print("Listing config")
            print(f"Kwargs: {kwargs}")

        def add_configuration(**kwargs):
            print("Adding config")
            print(f"Kwargs: {kwargs}")

        main("argparse.json", {
            "list_config": list_configuration,
            "add_config": add_configuration
        })

        The func_map key must match the JSON configuration file func value

Other benefits to the :meth:`spine.cli.setup.main` function are:

1. Automatically add the CLI version when passed :code:`cli_version`, allowing end users to run :code:`<name>.py --version`
2. Sets up the logging using :meth:`spine.log.config.setup` while defaulting to standard terminal logging output
3. It will automatically attempt to load any :code:`.env` files as environment variables using :meth:`spine.environ.load.load_env`

.. autofunction:: spine.cli.exc.main

setup
^^^^^

build
~~~~~
The :meth:`spine.cli.setup.build` function allows you to pass in a configuration file that generates the CLI command and argument structure.

An example JSON file would look like:

.. code-block:: JSON

    {
        "description": "Test CLI Description",
        "arguments": [
            {
                "type": "group",
                "arguments": [
                    {
                        "name": "--quiet",
                        "flag": null,
                        "dest": "quiet",
                        "help": "Quiet logging (only warning, error, or critical)",
                        "action": "store_true"
                    },
                    {
                        "name": "--verbose",
                        "flag": null,
                        "dest": "verbose",
                        "help": "Verbose logging output",
                        "action": "store_true"
                    }
                ]
            }
        ],
        "subparsers": [
            {
                "command": "config",
                "help": "View and modify configuration",
                "subparsers": [
                    {
                        "command": "list",
                        "help": "List configuration",
                        "defaults": {
                            "func": "list_config"
                        }
                    },
                    {
                        "command": "show",
                        "help": "Show configuration"
                    },
                    {
                        "command": "add",
                        "help": "Add configuration",
                        "arguments": [
                            {
                                "name": "--proxy",
                                "metavar": "N",
                                "nargs": "+",
                                "help": "Add proxy to configuration file"
                            },
                            {
                                "name": "--name",
                                "flag": "-n",
                                "dest": "name",
                                "help": "Name of the user for display"
                            }
                        ],
                        "defaults": {
                            "func": "add_config"
                        }
                    }
                ]
            }
        ]
    }


Running the CLI program :code:`<name>.py --help` would output:

.. code-block:: bash

    usage: <name> [-h] [--quiet | --verbose] {config} ...

    Test CLI Description

    positional arguments:
        {config}
            config    View and modify configuration

    options:
        -h, --help  show this help message and exit
        --quiet     Quiet logging (only warning, error, or critical)
        --verbose   Verbose logging output

Since this configuration has nested commands, you can run :code:`<name>.py config --help` to output:

.. code-block:: bash

    usage: <name> config [-h] {list,show,add} ...

    positional arguments:
        {list,show,add}
            list           List configuration
            show           Show configuration
            add            Add configuration

    options:
        -h, --help       show this help message and exit

.. autofunction:: spine.cli.setup.build

ver
^^^

add_version
~~~~~~~~~~~
The :meth:`spine.cli.ver.add_version` function adds the command line interface program version to the parser argument.

.. autofunction:: spine.cli.ver.add_version
