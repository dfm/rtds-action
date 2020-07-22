# -*- coding: utf-8 -*-

import os
import sphinx_material
from pkg_resources import DistributionNotFound, get_distribution

# Fanciness to get version number
try:
    __version__ = get_distribution("rtds_action").version
except DistributionNotFound:
    __version__ = "dev"


extensions = [
    # For processing notebooks
    "nbsphinx",
    # The topic of these docs
    "rtds_action",
    # Nicer docs
    "sphinx_copybutton",
]

# Settings for GitHub actions integration
rtds_action_github_repo = "dfm/rtds-action"
rtds_action_path = "tutorials"
rtds_action_artifact_prefix = "notebooks-for-"
rtds_action_github_token = os.environ.get("GITHUB_TOKEN", None)

# General settings
source_suffix = ".rst"
master_doc = "index"

project = "ReadTheDocs + GitHub Actions"
author = "Dan Foreman-Mackey"
copyright = "2020, " + author
version = __version__
release = __version__

exclude_patterns = ["_build"]

# HTML theme
html_show_sourcelink = False
html_sidebars = {
    "**": [
        "logo-text.html",
        "globaltoc.html",
        "localtoc.html",
        "searchbox.html",
    ]
}

extensions.append("sphinx_material")
html_theme_path = sphinx_material.html_theme_path()
html_context = sphinx_material.get_html_context()
html_theme = "sphinx_material"
html_title = "Interface ReadTheDocs and GitHub Actions"
html_short_title = "ReadTheDocs + GitHub Actions"
html_theme_options = {
    "nav_title": "rtds-action",
    "logo_icon": "&#xe869",
    "color_primary": "blue",
    "color_accent": "light-blue",
    "repo_url": "https://github.com/dfm/rtds-action",
    "repo_name": "rtds-action",
    "globaltoc_depth": 1,
    "globaltoc_collapse": False,
    "globaltoc_includehidden": False,
    "heroes": {
        "index": "Don't save executed Jupyter notebooks to your git repos "
        "ever again!"
    },
    "nav_links": [],
}
