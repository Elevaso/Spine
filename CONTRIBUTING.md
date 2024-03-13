# Contributing
When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change. 

Please note we have a [code of conduct](https://elevaso.atlassian.net/wiki/x/AQAf), please follow it in all your interactions with the project.

## Style Guide
This library leverages the python style guide as defined by [Google](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)

## Directory Structure
```
   .
   ├── .github                      # GitHub repository files
   ├── .gitlab                      # GitLab repository files
   ├── .vscode                      # Settings for Visual Studio Code
   ├── docs                         # Files for generating documentation
      ├── _static_                  # Directory for static HTML files (i.e. images)
      ├── _templates                # HTML template files
      ├── modules                   # Directory with ReStructured file for each sub-module
         └── <name>.rst             # File for each sub-module or Python file
      ├── advanced_usage.rst        # Advanced module usage instructions
      ├── change_log.rst            # Change log documentation
      ├── conf.py                   # Sphinx configuration file
      ├── contributing.rst          # Contributing documentation
      ├── description.rst           # Module description
      ├── getting_started.rst       # Basic getting started instructions
      ├── index.rst                 # Sphinx index file
      ├── license.rst               # Module LICENSE file
      ├── modules.rst               # Build module directory index
      ├── readme.rst                # Readme file
      ├── requirements.txt          # Module requirements
      ├── testing.rst               # Testing instructions
      └── versioning.rst            # Version details
   ├── src                          # Main code directory
      └── <name>                    # Name of the project
   ├── tests                        # Directory with test files
      └── unit                      # Directory with unit test files
        ├── context.py              # Common file for all test_*.py files to include
        └── test_<name>.py          # Test file for each python file in src/<name>
   ├── .codeclimate.yml             # Code quality configuration
   ├── .coveragerc                  # Code coverage configuration
   ├── .editorconfig                # File to help with editor differences by OS
   ├── .gitignore                   # Files/Directories to ignore for Git Version Control
   ├── .gitlab-ci.yml               # GitLab Continuous Integration file
   ├── .pypirc                      # PyPi configuration file
   ├── CHANGELOG.md                 # Log for each version
   ├── CONTRIBUTING.md              # Contributing to repo instructions
   ├── LICENSE                      # Project license
   ├── pylintrc.txt                 # PyLint configuration
   ├── pyproject.toml               # Project configuration
   ├── README.md                    # Main repo README file
   ├── requirements-dev.txt         # External python package requirements for contributing/development
   └── requirements.txt             # External python package requirements
```

## Built With
See our [Environment Setup](https://elevaso.atlassian.net/wiki/x/84AR) page for installation and configuration of local environment.

Below is a list of all external python libraries that are used for the development of this project, which can also be found in the [requirements-dev.txt](requirements-dev.txt) file located at the root of the project.

* __[black](https://pypi.org/project/black/)__ - For auto-formatting Python code in Visual Studio Code
* __[coverage](https://coverage.readthedocs.io/en/coverage-5.4/)__ - For evaluating test code coverage (lines of code covered by a test case)
* __[coverage-badge](https://github.com/dbrgn/coverage-badge)__ - For displaying the coverage percent in GitLab as a badge
* __[PyLint](https://pypi.org/project/pylint/)__ - Checking syntax and formatting during development
* __[recommonmark](https://recommonmark.readthedocs.io/en/latest/)__ - For parsing Markdown into ReStructured Text format (i.e. README.md into Sphix Documentation output)
* __[Sphinx](https://www.sphinx-doc.org/en/master/)__ - For generating documentation
* __[sphinxcontrib-mermaid](https://github.com/mgaitan/sphinxcontrib-mermaid)__ - For auto-generating function call dependencies
* __[sphinx-copybutton](https://sphinx-copybutton.readthedocs.io/en/latest/)__ - For adding copy button to code snippets
* __[sphinx-multiversion](https://holzhaus.github.io/sphinx-multiversion/master/index.html)__ - For generating documentation per version
* __[sphinx_rtd_theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/)__ - For ReadTheDocs.io Theme in sphinx documentation output
* __[unittest-xml-reporting](https://pypi.org/project/unittest-xml-reporting/)__ - For JUnit format to display in build pipeline output

## Code Merge
Prior to submitting merge requests, ensuring the following steps are complete:

- [ ] Update version and CHANGELOG.md file
- [ ] Run command for testing `python -m unittest discover tests/unit/`
- [ ] Run command for code testing coverage
    ```
    coverage run -m unittest discover tests/unit/
    coverage report -m
    ```
- [ ] Run command to generate docs and validate accuracy `rm -rf public/html && sphinx-build docs public/html`
- [ ] Run command to package module for distribution `py -m build`

## Code of Conduct
See our [Confluence Code of Conduct](https://elevaso.atlassian.net/wiki/x/AQAf) page for details.
