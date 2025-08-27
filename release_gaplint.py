#!/usr/bin/env python
"""
This module contains a script for releasing the Semigroups GAP package.
"""

import os
import re
import glob
import subprocess

from release import add_checks, exit_abort, exit_error, get_file_contents
from release import main as _main
from release import new_version, rc_branch, stable_branch, today, exec_string


def _check_setup_py_version_num():
    """
    Checks if the version in the setup.py file is the same as the
    releasing version.
    """
    regex = re.compile(r'version\s*=\s*"(\d+\.\d+\.\d+)"')
    match = regex.search(get_file_contents("setup.py"))
    if match:
        if match.group(1) != new_version():
            exit_abort(
                f"Version in setup.py is {match.group(1)} but version being released is {new_version()}"
            )
    else:
        exit_error("Cannot determine the version number in setup.py")
    return "ok!"


add_checks(
    ("checking for trailing whitespace", _check_setup_py_version_num),
)


def release_steps():
    "The release steps that will be displayed."
    return (
        f"git push origin {rc_branch()}",
        f"open a PR from {rc_branch()} to {stable_branch()} "
        f"(create {stable_branch()} if necessary):\n"
        + f"https://github.com/james-d-mitchell/digraphs/pull/new/{rc_branch()}"
        + " wait for the CI to complete successfully",
        f"git checkout {stable_branch()} && git merge {rc_branch()}",
        f"git branch -D {rc_branch()} && git push origin --delete {rc_branch()}",
        f"git checkout main && git merge {stable_branch()} && git push origin main",
    )


def main():
    "Run the release script"
    _main(release_steps, "release_gaplint")


if __name__ == "__main__":
    main()
