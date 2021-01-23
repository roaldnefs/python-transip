# Configuration file for the Sphinx documentation builder.
import os
import sys
from datetime import datetime

sys.path.append("../")
sys.path.append(os.path.dirname(__file__))
# sys.path.insert(0, os.path.abspath('..'))

import transip


# Project information
project = transip.__title__
copyright = '{}, {}'.format(
    datetime.now().year,
    transip.__author__
)
author = transip.__author__
version = transip.__version__
release = version

# General configuration
extensions = ['m2r2']
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
source_suffix = ['.rst', '.md']

# Options for HTML output
html_theme = 'alabaster'
html_theme_options = {
    "description": "Python wrapper for the TransIP API. It allows you to create, read and update resources on TransIP with ease using Python.",
    "show_powered_by": False,
    "github_user": "roaldnefs",
    "github_repo": "python-transip",
    "github_banner": True,
    "show_related": False,
    "note_bg": "#FFF59C",
}
html_static_path = ['_static']
