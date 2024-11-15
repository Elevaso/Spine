Getting Started
---------------

To get started using this module, make sure you have access to the `Elevaso GitLab PyPi Registry <https://gitlab.com/groups/elevaso/-/packages/?type=PyPI&version=&orderBy=created_at&sort=desc&search[]=>`_.

For easy access, you can update your local :code:`.pypirc` file, typically found in the home directory, with the following:


.. code-block:: ini

    [global]
    extra-index-url = https://__token__:{GITLAB_TOKEN}@gitlab.com/api/v4/groups/81835940/-/packages/pypi/simple # gitleaks:allow

Replace :code:`{GITLAB_TOKEN}` with your actual GitLab Personal Access Token.

Next, run an install and/or upgrade :code:`pip install --upgrade <project_name>`.

You can now import the library into your project by adding the following to your :code:`.py` file.

.. code-block:: python

    import <project_name>

.. note::

    Replace :code:`<project_name>` with |project| in the pip install and import code above.
