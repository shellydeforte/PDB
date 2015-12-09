# -*- coding: utf-8 -*-
"""Unit tests for fetch functions."""
from __future__ import (
    absolute_import, division, print_function, unicode_literals)

import os
import unittest

from pdb.driver_parse import fetch_and_write_files
from pdb.lib.data_paths import ProjectFolders

try:
    from StringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO        # Python 3


class TestMissingDirectories(unittest.TestCase):
    """Test when initial data already exists."""
    def test_dirs_is_not_ProjectFolders_instance(self):
        dirs = "Not an instance of ProjectFolders"
        self.assertRaises(
            AssertionError,
            fetch_and_write_files,
            dirs
        )
        return None

    def test_project_home_is_not_directory(self):
        working_dir = os.getcwd()
        dirs = ProjectFolders(
            user_home=None,
            project_home='not a directory',
            uni_data=working_dir,
            tsv_data=working_dir,
            working=working_dir
        )
        self.assertRaises(
            AssertionError,
            fetch_and_write_files,
            dirs
        )
        return None

    def test_dirs_uni_data_is_none(self):
        working_dir = os.getcwd()
        dirs = ProjectFolders(
            user_home=None,
            project_home=working_dir,
            uni_data=None,
            tsv_data=working_dir,
            working=working_dir
        )
        self.assertRaises(
            AssertionError,
            fetch_and_write_files,
            dirs
        )
        return None

    def test_dirs_tsv_data_is_none(self):
        working_dir = os.getcwd()
        dirs = ProjectFolders(
            user_home=None,
            project_home=working_dir,
            uni_data=working_dir,
            tsv_data=None,
            working=working_dir
        )
        self.assertRaises(
            AssertionError,
            fetch_and_write_files,
            dirs
        )
        return None

    def test_dirs_working_is_none(self):
        working_dir = os.getcwd()
        dirs = ProjectFolders(
            user_home=None,
            project_home=working_dir,
            uni_data=working_dir,
            tsv_data=working_dir,
            working=None
        )
        self.assertRaises(
            AssertionError,
            fetch_and_write_files,
            dirs
        )
        return None


if __name__ == '__main__':
    unittest.main()
