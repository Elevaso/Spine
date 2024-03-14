Getting Started
---------------

To get started using this module, make sure you have access to the `Elevaso GitLab PyPi Registry <https://gitlab.com/api/v4/groups/81835940/packages/pypi>`_.

For easy access, you can update your local :code:`.pypirc` file, typically found in the home directory, with the following:


.. code-block:: ini

    [distutils]
    index-servers =
      elevaso
      pypi

    [pypi]
    repository = https://upload.pypi.org/legacy/

    [elevaso]
    repository = https://gitlab.com/api/v4/groups/81835940/packages/pypi
    username = ${env.GITLAB_TOKEN_NAME}
    password = ${env.GITLAB_TOKEN}

This will authenticate to GitLab PyPi for Elevaso using your GitLab personal access token. Your token name and value will need to be stored in environment variables :code:`GITLAB_TOKEN_NAME` and :code:`GITLAB_TOKEN` respectively. Optionally, you can replace the :code:`${env.GITLAB_TOKEN_NAME}` and :code:`${env.GITLAB_TOKEN}` with the actual values

Next, run an install and/or upgrade :code:`pip install --upgrade <project_name>`.

You can now import the library into your project by adding the following to your :code:`.py` file.

.. code-block:: python

    import <project_name>

.. note::

    Replace :code:`<project_name>` with |project| in the pip install and import code above.
