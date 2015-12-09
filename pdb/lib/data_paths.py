# -*- coding: utf-8 -*-
"""Process and store project directory path names."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os

from collections import namedtuple


def find_home_dir():
    """Attempt to find the user's home directory."""
    if os.path.expanduser('~'):
        # Try to find home in a platform independent way.
        home = os.path.expanduser('~')
    elif os.getenv('HOME'):
        # Find home on Posix machines.
        home = os.getenv('HOME')
        # Find home on Windows machines.
    elif os.getenv('USERPROFILE'):
        home = os.getenv('USERPROFILE')
    else:
        home = os.getcwd()
        print(
            "Unable to determine user's home directory.\n"
            "Using current working directory instead:\n"
            "\t{}".format(home)
        )
    return home


ProjectFolders_ = namedtuple(
    'ProjectFolders', [
        'user_home',
        'project_home',  # Top level directory for project.
        'uni_data',
        'tsv_data',
        'working'       # Directory for intermediary data storage.
    ]
)


ProjectFolders_.__new__.__defaults__ = (
    None,
    None,
    None,
    None,
    None
)


class ProjectFolders(ProjectFolders_):
    """Path names for project directories and subdirectories.

    Note that ProjectFolder should be used with its constructor
    as opposed to assigning values to fields directly.

    Correct example:
        dirs = ProjectFolders(
            user_home=user_home,

            project_home=project_dir,

            uni_data=uni_folder,

            tsv_data=tsv_folder,

            working=working_folder)

    Using a new directory path after assignment:
        updated_dirs = dirs._replace(working=new_temp_folder)

    Incorrect example:
        dirs = ProjectFolders

        dirs.user_home = user_home

    """
    pass


def build_abs_path(folder_path, uni_id):
    """Return absolute path for directory and file name."""
    uni_fn = ''.join([uni_id, '.fasta'])
    uni_fp = os.path.join(folder_path, uni_fn)
    return uni_fp
