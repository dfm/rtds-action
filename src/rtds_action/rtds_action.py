# -*- coding: utf-8 -*-

__all__ = ["setup"]

import subprocess
from io import BytesIO
from zipfile import ZipFile

import requests
from sphinx.util import logging
from sphinx.errors import ExtensionError

logger = logging.getLogger(__name__)


def config_inited(app, config):
    prefix = config["rtds_action_artifact_prefix"]
    path = config["rtds_action_path"]
    repo = config["rtds_action_github_repo"]
    if repo is None:
        raise ExtensionError(
            "rtds_action: missing required argument 'rtds_action_github_repo'"
        )
    token = config["rtds_action_github_token"]
    if token is None:
        raise ExtensionError(
            "rtds_action: missing required argument 'rtds_action_github_token'"
        )

    try:
        git_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .strip()
            .decode("ascii")
        )
    except subprocess.CalledProcessError:
        logger.warn("rtds_action: can't get git hash")
        return

    r = requests.get(
        f"https://api.github.com/repos/{repo}/actions/artifacts",
        params=dict(per_page=100),
    )
    if r.status_code != 200:
        logger.warn(f"Can't list files ({r.status_code})")
        return

    expected_name = f"{prefix}{git_hash}"
    result = r.json()
    for artifact in result.get("artifacts", []):
        if artifact["name"] == expected_name:
            logger.info(artifact)
            r = requests.get(
                artifact["archive_download_url"],
                headers={"Authorization": f"token {token}"},
            )

            if r.status_code != 200:
                logger.warn(f"Can't download artifact ({r.status_code})")
                return

            with ZipFile(BytesIO(r.content)) as f:
                f.extractall(path=path)

            return

    logger.warn("rtds_action: can't find expected artifact")


def setup(app):
    app.add_config_value("rtds_action_artifact_prefix", "", rebuild="env")
    app.add_config_value("rtds_action_path", ".", rebuild="env")
    app.add_config_value("rtds_action_github_repo", None, rebuild="env")
    app.add_config_value("rtds_action_github_token", None, rebuild="env")
    app.connect("config-inited", config_inited)
