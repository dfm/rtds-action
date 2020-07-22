# -*- coding: utf-8 -*-

import os

extensions = ["nbsphinx", "rtds_action"]

rtds_action_github_repo = "dfm/rtds-action"
rtds_action_path = "tutorials"
rtds_action_artifact_prefix = "notebooks-for-"
rtds_action_github_token = os.environ.get("GITHUB_TOKEN", None)

source_suffix = ".rst"
master_doc = "index"

project = "rtds-action"
author = "Dan Foreman-Mackey"
copyright = "2020, " + author
version = "0.1.0"
release = "0.1.0"

exclude_patterns = ["_build"]
