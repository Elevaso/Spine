# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# Python Standard Libraries
import codecs
import os.path
import re
import sys

# 3rd Party Libraries
import tomli

ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..")

sys.path.append(os.path.join(ROOT, "src"))

def read(*parts):
    with open(os.path.join(ROOT, "src", *parts), "r") as f:
        return f.read()

    return codecs.open(os.path.join(ROOT, "src", *parts), 'r').read()

def find_version(*file_paths):
    for i in os.listdir(os.path.join(ROOT, "src")):
        version_file = read(os.path.join(ROOT, "src", i, "__init__.py"))
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
        if version_match:
            return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

# -- Project information -----------------------------------------------------
with open(os.path.join(ROOT, "pyproject.toml"), "rb") as f:
    project_data = tomli.load(f)

project = project_data["project"]["name"]
description = project_data["project"]["description"]
copyright = project_data["project"].get("copyright", "")
version = project_data["project"].get("version", find_version())

rst_prolog = f"""
.. |project| replace:: {project}
.. |description| replace:: {description}
"""

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # "recommonmark",
    "sphinx.ext.autodoc",
    "sphinxcontrib.mermaid",
    "sphinx_rtd_theme",
    "sphinx.ext.todo",
    "sphinx_multiversion",
    "sphinx.ext.viewcode",  # Add links to highlighted source code
    "sphinx_mdinclude", # Markdown reader
]

todo_include_todos = True

autosectionlabel_prefix_document = True

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_logo = '_static/icon.svg'

html_css_files = [
    'css/main.css',
]

html_sidebars = {
    "**": [
        "versions.html",
    ]
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "canonical_url": "",
    # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": True,
    # 'vcs_pageview_mode': '',
    "style_nav_header_background": "#404040",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# These settings allow for multi-version documentation to co-exist
# https://holzhaus.github.io/sphinx-multiversion/master/configuration.html#configuration

smv_tag_whitelist = r'^.*$'

smv_branch_whitelist = r'^(main)$' # Only the main branch

smv_remote_whitelist = r'^(origin|upstream)$' # Only origin/remote branches
