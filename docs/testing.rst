.. _section-license:

Testing
=======
Many tests have been scripted to allow for validating the functionality of this library.

Guidelines
----------
All project code should have test cases built that cover the possible scenarios/values, and validate proper error handling. Generally speaking, each line of code should have "coverage" of a test case.

Unit Test
---------
Python's `unit_test` library is used for test cases against functions and classes. To run all tests, you can run the following command:

.. code-block:: python
   :linenos:

   python -m unittest discover tests/unit/

The output will be the number of tests executed and the successful count.

Code Coverage
-------------
A code coverage report is generated during each build to identify portions of code where a unit test case is not executed.

To execute this locally, run the following command:

.. code-block:: python
   :linenos:

   coverage run -m unittest discover tests/unit/
   coverage report -m

Reports
^^^^^^^

.. raw:: html

    <ul id="coverage"></ul>
    <script>
        var ul = document.getElementById("coverage");

        fetch("./coverage.json")
            .then((response) => {
            return response.json();
            })
            .then((data) => {
            let json = data;

            for (let i = 0; i < json.length; i++){
                var li = document.createElement("li");

                ul.appendChild(li);
                li.innerHTML="<a href=\"coverage/" + json[i] +"\" target=\"_blank\">" + json[i] + "</a>";
            }
            })
            .catch(function(){
            var li = document.createElement("li");

            ul.appendChild(li);
            li.innerHTML="No reports available";
            });
    </script>

Code Climate
------------
In addition to the above tests, a Code Climate report is run during the build process to validate against best practices.

The file ``.codeclimate.yml`` contains the modules for use and the configuration of values.

The following modules are enabled for scanning the code:

* `Bandit <https://docs.codeclimate.com/docs/bandit>`_: Checks Python code for common security issues
* `EditorConfig <https://docs.codeclimate.com/docs/editorconfig>`_: Checks files against ``.editorconfig`` file configuration
* `FIXME <https://docs.codeclimate.com/docs/fixme>`_: Checks for ``TODO``, ``FIXME``, ``BUG`` comments
* `PEP8 <https://docs.codeclimate.com/docs/pep8>`_: Formatting best practices
* `pylint <https://docs.codeclimate.com/docs/pylint>`_: Linting and formatting of code
* `Sonar Python <https://docs.codeclimate.com/docs/sonar-python>`_: Bugs, security, complexity, and other best practices
