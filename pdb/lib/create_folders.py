# -*- coding: utf-8 -*-
"""Create project folders."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os

from pdb.lib.data_paths import ProjectFolders


def create_folders(dirs):
    """Create project folders.

    Create data folders for the project. The working_subdir, uni_subdir,
    and tsv_subdir names will be created as subdirectories under
    the project_folder name.

    Args:
        dirs (ProjectFolders): A named tuple with the project folder names.

    Returns:
        None

    """
    # All ProjectFolder paths are required except user_home.
    assert dirs.project_home
    assert dirs.uni_data
    assert dirs.tsv_data
    assert dirs.working

    if not os.path.isdir(dirs.project_home):
        assert not os.path.exists(dirs.project_home)
        os.makedirs(dirs.project_home)
        assert os.path.isdir(dirs.project_home)

    if not os.path.isdir(dirs.uni_data):
        assert not os.path.exists(dirs.uni_data)
        os.makedirs(dirs.uni_data)
        assert os.path.isdir(dirs.uni_data)

    if not os.path.isdir(dirs.tsv_data):
        assert not os.path.exists(dirs.tsv_data)
        os.makedirs(dirs.tsv_data)
        assert os.path.isdir(dirs.tsv_data)

    if not os.path.isdir(dirs.working):
        assert not os.path.exists(dirs.working)
        os.makedirs(dirs.working)
        assert os.path.isdir(dirs.working)

    return None
