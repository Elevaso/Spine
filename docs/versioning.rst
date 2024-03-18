.. _section-versioning:

This project uses the |Semantic Versioning|, which consists of MAJOR.MINOR.PATCH, and follows the best practices of change log usage from |KeepAChangeLog|.

A CHANGELOG file tracks all the changes by version in friendly format, with the format of:

.. code-block:: md
   :linenos:

   ## Unreleased
      - <Change Type>
         1. <Description>
         2. <Description>

   ## ##.##.## - MON DD, YYYY
      - <Change Type>
         1. <Description>
               - Module(s): <module>, <module>
         2. <Description>
               - Module(s): <module>, <module>

Where the following placeholders are used as:

+--------------+--------------------------------------------------------------------------------+
| Type         | Description                                                                    |
+==============+================================================================================+
| type         | Type of change, with acceptable values of                                      |
|              |  * **Added**: New features                                                     |
|              |  * **Changed**: Updates to existing features                                   |
|              |  * **Deprecated**: Soon-to-be removed features                                 |
|              |  * **Removed**: Now removed features                                           |
|              |  * **Fixed**: Bug fixes                                                        |
|              |  * **Security**: Vulnerability fixes                                           |
+--------------+--------------------------------------------------------------------------------+
| module       | List of file(s) the change applies to                                          |
+--------------+--------------------------------------------------------------------------------+
| description  | Description of the change made                                                 |
+--------------+--------------------------------------------------------------------------------+

Changes are displayed in descending order (most recent first), with an UNRELEASED section at the very top for changes that are pending.

.. |Semantic Versioning| raw:: html
   
   <a href="https://semver.org/" target="_blank">Semantic Versioning</a>

.. |KeepAChangeLog| raw:: html

   <a href="https://keepachangelog.com/en/1.0.0/" target="_blank">KeepAChangeLog</a>
